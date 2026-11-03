import { test, expect, openLab, expectNoSideScroll } from '../fixtures';

test('works when the browser refuses storage (private windows)', async ({ page, academy }) => {
  await page.addInitScript(() => {
    const refuse = () => { throw new DOMException('The quota has been exceeded.', 'QuotaExceededError'); };
    Storage.prototype.getItem = refuse;
    Storage.prototype.setItem = refuse;
    Storage.prototype.removeItem = refuse;
  });
  await page.goto(academy.url);
  await page.getByRole('button', { name: 'Start learning' }).first().click();
  await page.getByLabel('Your name').fill('Ada');
  await page.getByLabel('Your name').press('Enter');
  await expect(page.locator('#now h2')).toHaveText('Next: Your First Commands');
  await expect(page.locator('#hello')).toContainText('Ada');
  // The theme toggle still works, it just isn't remembered.
  const before = await page.locator('html').getAttribute('data-theme');
  await page.locator('#btn-theme').click();
  await expect(page.locator('html')).not.toHaveAttribute('data-theme', before!);
});

test('says so on the page when the server cannot be reached', async ({ page, academy, consoleErrors }) => {
  await page.route('**/api/**', r => r.abort());
  await page.goto(academy.url + '#lab');
  const alert = page.getByRole('alert').filter({ hasText: 'The lab did not load' });
  await expect(alert).toBeVisible();
  await expect(alert).toContainText('./run.sh');
  await expect(alert.getByRole('button', { name: 'Reload' })).toBeVisible();
  consoleErrors.length = 0;  // the aborted requests are logged by the browser itself
});

test('keyboard: enter the lab, open and close the lesson', async ({ page, academy, browserName }) => {
  test.skip(test.info().project.name.startsWith('mobile'), 'no hardware keyboard on phones');
  await page.goto(academy.url);
  // Tab reaches Start learning (WebKit only tabs to links/buttons with this macOS setting, so focus it directly there).
  const enter = page.locator('#btn-enter');
  if (browserName === 'webkit') await enter.focus();
  else {
    for (let i = 0; i < 15 && !(await enter.evaluate(el => el === document.activeElement)); i++) await page.keyboard.press('Tab');
  }
  await expect(enter).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.getByLabel('Your name')).toBeFocused();
  await page.keyboard.type('Ada');
  await page.keyboard.press('Enter');
  await expect(page.locator('#now h2')).toBeVisible();

  await page.locator('#now-read').focus();
  await page.keyboard.press('Enter');
  const reader = page.locator('#reader');
  await expect(reader).toBeVisible();
  await expect(page.locator('#reader-x')).toBeFocused();
  // Tab stays inside the open dialog.
  for (let i = 0; i < 8; i++) {
    await page.keyboard.press('Tab');
    expect(await page.evaluate(() => !!document.activeElement?.closest('#reader'))).toBe(true);
  }
  await page.keyboard.press('Escape');
  await expect(reader).toBeHidden();
  await expect(page.locator('#now-read')).toBeFocused();
});

test('focus is visible on buttons', async ({ page, academy }) => {
  test.skip(test.info().project.name.startsWith('mobile'), 'no hardware keyboard on phones');
  await openLab(page, academy);
  await page.locator('#now-start').focus();
  await page.keyboard.press('Shift+Tab');
  await page.keyboard.press('Tab');
  const outline = await page.locator('#now-start').evaluate(el => getComputedStyle(el).outlineStyle);
  expect(outline).not.toBe('none');
});

for (const hash of ['', '#lab', '#dojo/intro-lab', '#profile']) {
  test(`no sideways scroll on ${hash || 'the intro'}`, async ({ page, academy }) => {
    await page.addInitScript(() => { try { localStorage.setItem('academy-player-name', 'Ada'); } catch {} });
    await page.goto(academy.url + hash);
    await page.waitForLoadState('networkidle');
    await expectNoSideScroll(page);
  });
}

test('fonts load from the server', async ({ page, academy }) => {
  await openLab(page, academy);
  const ok = await page.evaluate(async () => {
    await document.fonts.ready;
    return document.fonts.check('16px Geist') && [...document.fonts].some(f => f.family.includes('Geist') && f.status === 'loaded');
  });
  expect(ok).toBe(true);
});

test('typing a flag on a phone keyboard is not auto-capitalised and does not zoom', async ({ page, academy }) => {
  await openLab(page, academy);
  const flag = page.locator('#now-flag');
  await expect(flag).toHaveAttribute('autocapitalize', 'none');
  await expect(flag).toHaveAttribute('autocorrect', 'off');
  const size = await flag.evaluate(el => parseFloat(getComputedStyle(el).fontSize));
  if ((page.viewportSize()?.width ?? 1000) <= 700) expect(size).toBeGreaterThanOrEqual(16);
});
