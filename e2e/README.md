# Browser tests

End-to-end tests for the dojo page (`platform/academy/static/dojo.html`), run with Playwright.
Each test starts its own academy server on a random port with empty progress and its own
challenge folder, and does the terminal part of a challenge by running the reference answer
in that folder (the same answers `scripts/verify_answers.py` uses).

```bash
cd e2e
npm ci
npx playwright install --with-deps    # once: downloads Chromium, Firefox and WebKit
npx playwright test                   # all five projects
npx playwright test --project=webkit  # one browser
npx playwright show-report            # after a failure
```

Projects: `chromium`, `firefox`, `webkit` (desktop) and `mobile-chrome` (Pixel 7),
`mobile-safari` (iPhone 13). The mobile ones are emulation in the desktop engines, not real phones.

What is covered:

- `first-challenges.spec.ts`: a new learner names themselves, does the first three challenges
  (Start, work, Mark as done, Next challenge), and progress survives a reload. Also an unfinished
  answer, hints (including pressing Hint quickly), feedback after a challenge, Restart, and starting
  from a belt page.
- `robustness.spec.ts`: storage refused (private windows), server unreachable, keyboard use and
  focus, no sideways scrolling, fonts, phone keyboard settings on the flag box. Any console error
  or page error fails the test that caused it.
- `accessibility.spec.ts`: axe-core on every screen and the challenge-complete dialog, in light and dark mode.

The tests need Python 3 and bash; they use the same `python3` the academy runs on.
