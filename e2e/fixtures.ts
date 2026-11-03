import { test as base, expect, type Page } from '@playwright/test';
import { spawn, execFileSync, type ChildProcess } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

export const ROOT = path.resolve(__dirname, '..');
const CHALLENGES = path.join(ROOT, 'curriculum/modules/18-zero-terminal/challenges');

export type Academy = {
  url: string;
  workspace: string;
  /** Do a challenge the way a learner would in their terminal: the reference answer, run in the folder. */
  solve(cid: string): void;
  /** Run shell commands in the challenge folder. */
  sh(script: string): void;
};

async function waitForServer(url: string, proc: ChildProcess, log: () => string) {
  for (let i = 0; i < 100; i++) {
    if (proc.exitCode !== null) throw new Error('academy server exited:\n' + log());
    try {
      if ((await fetch(url + 'api/me')).ok) return;
    } catch {}
    await new Promise(r => setTimeout(r, 100));
  }
  throw new Error('academy server did not start:\n' + log());
}

export const test = base.extend<{ academy: Academy; consoleErrors: string[] }>({
  academy: async ({}, use) => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'academy-e2e-'));
    const workspace = path.join(dir, 'ws');
    let proc: ChildProcess | undefined, url = '', out = '';
    // A random free-looking port; retry if another test grabbed it first.
    for (let attempt = 0; attempt < 5 && !url; attempt++) {
      const port = 20000 + Math.floor(Math.random() * 20000);
      out = '';
      proc = spawn('python3', ['-m', 'academy.cli', 'serve', '--local', '--host', '127.0.0.1', '--port', String(port)], {
        cwd: ROOT,
        env: {
          ...process.env,
          PYTHONPATH: ['vendor', 'platform'].map(p => path.join(ROOT, p)).join(path.delimiter),
          ACADEMY_CURRICULUM: path.join(ROOT, 'curriculum'),
          ACADEMY_DATA: path.join(dir, 'data'),
          ACADEMY_WORKSPACE: workspace,
          ACADEMY_FLAG_PATH: path.join(dir, 'flag.txt'),
          ACADEMY_OPEN_TERMINAL: '0',
        },
        stdio: ['ignore', 'pipe', 'pipe'],
      });
      proc.stdout!.on('data', d => (out += d));
      proc.stderr!.on('data', d => (out += d));
      try {
        await waitForServer(`http://127.0.0.1:${port}/`, proc, () => out);
        url = `http://127.0.0.1:${port}/`;
      } catch (e) {
        proc.kill();
        if (attempt === 4) throw e;
      }
    }
    const run = (script: string) => execFileSync('bash', ['-c', script], { cwd: workspace, env: { ...process.env, HOME: workspace } });
    await use({
      url,
      workspace,
      solve(cid) {
        const solution = path.join(CHALLENGES, cid, 'solution');
        for (const name of fs.readdirSync(solution)) {
          if (name !== 'solve.sh') fs.cpSync(path.join(solution, name), path.join(workspace, name), { recursive: true });
        }
        if (fs.existsSync(path.join(solution, 'solve.sh'))) run(`bash "${path.join(solution, 'solve.sh')}"`);
      },
      sh: run,
    });
    proc!.kill();
    fs.rmSync(dir, { recursive: true, force: true });
  },

  // Every page error or console error fails the test that caused it.
  consoleErrors: [async ({ page }, use) => {
    const errors: string[] = [];
    page.on('pageerror', e => errors.push('page error: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push('console error: ' + m.text()); });
    await use(errors);
    expect(errors, 'the page logged errors').toEqual([]);
  }, { auto: true }],

  page: async ({ page }, use) => {
    // Skip the motion so screenshots and clicks don't wait on animations.
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await use(page);
  },
});

export { expect };

/** Open the lab as a returning learner who already chose a name. */
export async function openLab(page: Page, academy: Academy, name = 'Ada') {
  await page.addInitScript(n => { try { localStorage.setItem('academy-player-name', n); } catch {} }, name);
  await page.goto(academy.url + '#lab');
  await expect(page.locator('#now h2')).toBeVisible();
}

/** The page must never scroll sideways. */
export async function expectNoSideScroll(page: Page) {
  const extra = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(extra, 'page is wider than the screen').toBeLessThanOrEqual(0);
}
