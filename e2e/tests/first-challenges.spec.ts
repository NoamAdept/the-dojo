import fs from 'node:fs';
import path from 'node:path';
import { test, expect, openLab, expectNoSideScroll } from '../fixtures';

// The path a new learner takes: name, Start, work in the terminal, Mark as done, next challenge.
const FIRST = [
  { id: 'zt-first-commands', title: 'Your First Commands' },
  { id: 'zt-files-folders', title: 'Files and Folders' },
  { id: 'zt-vim-cat', title: 'Creating and Editing Text Files' },
];

test('a new learner completes the first three challenges', async ({ page, academy }) => {
  await page.goto(academy.url);
  await page.getByRole('button', { name: 'Start learning' }).first().click();
  const gate = page.getByRole('dialog', { name: 'What should we call you?' });
  await expect(gate).toBeVisible();
  await page.getByLabel('Your name').fill('Ada');
  await page.getByRole('button', { name: 'Save and enter' }).click();
  await expect(gate).toBeHidden();

  for (const [i, ch] of FIRST.entries()) {
    const now = page.locator('#now');
    await expect(now.locator('h2')).toHaveText(`Next: ${ch.title}`);
    await expect(now.getByRole('button', { name: 'Mark as done' })).toBeDisabled();
    await now.getByRole('button', { name: 'Start' }).click();
    await expect(page.locator('#now-ws')).toContainText(academy.workspace);
    await expectNoSideScroll(page);

    academy.solve(ch.id);
    await now.getByRole('button', { name: 'Mark as done' }).click();
    const cele = page.locator('#celebrate');
    await expect(cele).toBeVisible();
    await expect(cele).toContainText(`${i + 1} / 110 challenges`);
    await expect(page.locator('#progress')).toHaveText(`${i + 1}/110`);
    await page.getByRole('button', { name: 'Next challenge' }).click();
    await expect(cele).toBeHidden();
  }
  await expect(page.locator('#now h2')).toHaveText('Next: Running Programs and Reading Errors');

  // Progress is kept by the server: a reload shows the same place.
  await page.goto('about:blank');  // a fresh load: WebKit treats a same-URL goto with a hash as an in-page jump
  await page.goto(academy.url + '#lab');
  await expect(page.locator('#now h2')).toHaveText('Next: Running Programs and Reading Errors');
  await expect(page.locator('#progress')).toHaveText('3/110');
});

test('an unfinished answer explains what is left and does not complete', async ({ page, academy }) => {
  await openLab(page, academy);
  await page.locator('#now-start').click();
  await expect(page.locator('#now-ws')).toBeVisible();
  academy.sh('echo Hello terminal > hello.txt; whoami > me.txt');

  await page.locator('#now-done').click();
  const fb = page.locator('#now-fb');
  await expect(fb).toContainText('Not done yet');
  await expect(fb).toContainText('2/4 tasks pass');
  await expect(fb).toContainText('today.txt');
  await expect(fb).not.toContainText('hello.txt:');
  await expect(fb).not.toContainText('AssertionError');
  await expect(page.locator('#celebrate')).toBeHidden();
  await expect(page.locator('#progress')).toHaveText('0/110');
});

test('hints open one at a time, and pressing Hint fast never repeats one', async ({ page, academy }) => {
  await openLab(page, academy);
  const hints = page.locator('#now-hints .h');
  const btn = page.locator('#now-hint');
  await btn.click();
  await expect(hints).toHaveCount(1);
  await expect(hints.first()).toContainText('Hint 1 of 3');
  // Spam the button: each press waits for the last, and it stops at the last hint.
  for (let i = 0; i < 6; i++) await btn.click({ force: true, noWaitAfter: true }).catch(() => {});
  await expect(btn).toHaveText('All hints shown');
  await expect(btn).toBeDisabled();
  await expect(hints).toHaveCount(3);
  await expect(hints.nth(2)).toContainText('Hint 3 of 3');
  // After a reload the button opens the hints already seen, not new ones.
  await page.reload();
  await btn.click();
  await expect(hints).toHaveCount(3);
  await expect(btn).toBeDisabled();
});

test('the learner can leave feedback when a challenge is done, and can skip it', async ({ page, academy }) => {
  const saved = path.join(path.dirname(academy.workspace), 'data', 'feedback.jsonl');
  await openLab(page, academy);
  const cele = page.locator('#celebrate');

  await page.locator('#now-start').click();
  await expect(page.locator('#now-ws')).toBeVisible();
  academy.solve('zt-first-commands');
  await page.locator('#now-done').click();
  await expect(cele).toBeVisible();
  const rate = cele.getByRole('button', { name: 'Too hard' });
  await rate.click();
  await expect(rate).toHaveAttribute('aria-pressed', 'true');
  await cele.getByLabel('Anything unclear or broken? (optional)').fill('Task 3 was   confusing');
  await cele.getByRole('button', { name: 'Next challenge' }).click();
  await expect(cele).toBeHidden();
  await expect(page.getByText('Thanks for the feedback')).toBeVisible();
  const lines = fs.readFileSync(saved, 'utf8').trim().split('\n').map(l => JSON.parse(l));
  expect(lines).toHaveLength(1);
  expect(lines[0]).toMatchObject({ challenge: 'zt-first-commands', rating: 'too-hard', note: 'Task 3 was confusing' });

  // Feedback is optional: Next works with nothing filled in, and nothing more is saved.
  await page.locator('#now-start').click();
  await expect(page.locator('#now-ws')).toBeVisible();
  academy.solve('zt-files-folders');
  await page.locator('#now-done').click();
  await expect(cele).toBeVisible();
  await expect(cele.getByRole('button', { name: 'Too hard' })).toHaveAttribute('aria-pressed', 'false');
  await expect(cele.getByLabel('Anything unclear or broken? (optional)')).toHaveValue('');
  await cele.getByRole('button', { name: 'Next challenge' }).click();
  await expect(cele).toBeHidden();
  expect(fs.readFileSync(saved, 'utf8').trim().split('\n')).toHaveLength(1);
});

test('Restart asks first, then puts the starter files back', async ({ page, academy }) => {
  await openLab(page, academy);
  await page.locator('#now-start').click();
  await expect(page.locator('#now-start')).toHaveText('Restart');
  academy.sh('echo Hello terminal > hello.txt');

  page.once('dialog', d => d.dismiss());
  await page.locator('#now-start').click();
  await expect(page.locator('#now-fb')).not.toContainText('Starting');
  academy.sh('test -f hello.txt');  // kept: the learner said no

  page.once('dialog', d => d.accept());
  await page.locator('#now-start').click();
  await expect(page.locator('#now-fb')).toContainText('Started');
  academy.sh('test ! -e hello.txt');
});

test('a belt page lists its challenges and starts one', async ({ page, academy }) => {
  await openLab(page, academy);
  await page.getByRole('button', { name: /Terminal from Zero/ }).click();
  const row = page.locator('.crow.open');
  await expect(row.locator('h3')).toHaveText('Your First Commands');
  await expect(row.getByRole('button', { name: 'Mark as done' })).toBeDisabled();
  await row.getByRole('button', { name: 'Start', exact: true }).click();
  await expect(row.getByRole('button', { name: 'Mark as done' })).toBeEnabled();
  academy.solve('zt-first-commands');
  await row.getByRole('button', { name: 'Mark as done' }).click();
  await expect(page.locator('#celebrate')).toBeVisible();
  await expectNoSideScroll(page);
});
