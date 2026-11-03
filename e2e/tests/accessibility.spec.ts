import fs from 'node:fs';
import { test, expect, openLab } from '../fixtures';

const AXE = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8');

// axe-core finds missing labels, low contrast, bad ARIA and similar problems automatically.
async function seriousProblems(page) {
  await page.addScriptTag({ content: AXE });
  return page.evaluate(async () => {
    const r = await (window as any).axe.run(document, { resultTypes: ['violations'] });
    return r.violations
      .filter(v => v.impact === 'serious' || v.impact === 'critical')
      .map(v => `${v.id}: ${v.nodes.map(n => n.target.join(' ')).join(', ')}`);
  });
}

for (const theme of ['light', 'dark'] as const) {
  for (const hash of ['', '#lab', '#dojo/intro-lab', '#profile']) {
    test(`${theme}: ${hash || 'intro'} has no serious accessibility problems`, async ({ page, academy }) => {
      await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
      await page.addInitScript(() => { try { localStorage.setItem('academy-player-name', 'Ada'); } catch {} });
      await page.goto(academy.url + hash);
      await page.waitForLoadState('networkidle');
      expect(await seriousProblems(page)).toEqual([]);
    });
  }
}

test('the lesson reader has no serious accessibility problems', async ({ page, academy }) => {
  await openLab(page, academy);
  await page.locator('#now-read').click();
  await expect(page.locator('#reader')).toBeVisible();
  expect(await seriousProblems(page)).toEqual([]);
});

for (const theme of ['light', 'dark'] as const) {
  test(`${theme}: the challenge-complete dialog and its feedback form have no serious accessibility problems`, async ({ page, academy }) => {
    await page.emulateMedia({ colorScheme: theme, reducedMotion: 'reduce' });
    await openLab(page, academy);
    await page.locator('#now-start').click();
    await expect(page.locator('#now-ws')).toBeVisible();
    academy.solve('zt-first-commands');
    await page.locator('#now-done').click();
    await expect(page.locator('#celebrate')).toBeVisible();
    await page.locator('#celebrate').getByRole('button', { name: 'About right' }).click();
    expect(await seriousProblems(page)).toEqual([]);
  });
}
