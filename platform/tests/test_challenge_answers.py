"""Every challenge: the starter fails, the reference answer passes, and the checks accept
every right answer in answer_cases.py and reject every wrong one."""

from __future__ import annotations

import itertools

import pytest

from answer_cases import COMMANDS, EDITS, FLAGS, SCRIPTS, Edit, Write
from challenge_harness import Lab, write_files

@pytest.fixture(scope="module")
def lab():
    lab = Lab()
    yield lab
    lab.close()


def all_challenges():
    lab = Lab()
    try:
        return [c.id for m in lab.engine.modules for c in lab.engine.module_challenges(m.slug)]
    finally:
        lab.close()


def describe(cid, n, answer, res):
    return f"{cid} task {n}: answer {answer!r}\n--- ./check said:\n{res.output[-1500:]}"


@pytest.mark.parametrize("cid", all_challenges())
def test_starter_fails_and_reference_passes(lab, cid):
    """Achievability: the reference answer reaches CHECK_OK from the starting files."""
    ws = lab.stage(cid, solution=False)
    if not (ws / "check").exists():
        pytest.skip("flag hunt: covered by test_flag_hunts")
    assert not lab.check(ws).ok, "the untouched starter must not pass"
    ws = lab.stage(cid, solution=True)
    res = lab.check(ws)
    assert res.ok, res.output[-2000:]


@pytest.mark.parametrize("cid", sorted(SCRIPTS))
def test_script_answers(lab, cid):
    """One ./check run tries a different answers/taskN.sh for every task at once."""
    problems = []
    for want in ("ok", "bad"):
        rows = {n: getattr(case, want) for n, case in SCRIPTS[cid].items()}
        for round_ in itertools.zip_longest(*[[(n, a) for a in answers] for n, answers in rows.items()]):
            tried = [x for x in round_ if x]
            ws = lab.stage(cid, solution=True)
            for n, body in tried:
                write_files(ws, {f"answers/task{n}.sh": "#!/bin/bash\n" + body + "\n"})
            res = lab.check(ws)
            for n, body in tried:
                if res.task_passes(n) != (want == "ok"):
                    problems.append(("should pass" if want == "ok" else "should fail") + " | " + describe(cid, n, body, res))
    assert not problems, "\n\n".join(problems)


@pytest.mark.parametrize("cid", sorted(COMMANDS))
def test_typed_commands(lab, cid):
    problems = []
    for n, case in COMMANDS[cid].items():
        for want, answers in (("ok", case.ok), ("bad", case.bad)):
            for commands in answers:
                ws = lab.stage(cid, solution=False)
                lab.sh(ws, commands)
                res = lab.check(ws)
                passed = res.ok if n is None else res.task_passes(n)
                if passed != (want == "ok"):
                    problems.append(("should pass" if want == "ok" else "should fail") + " | " + describe(cid, n, commands, res))
    assert not problems, "\n\n".join(problems)


@pytest.mark.parametrize("cid", sorted(EDITS))
def test_edited_answers(lab, cid):
    problems = []
    for n, case in EDITS[cid].items():
        for want, answers in (("ok", case.ok), ("bad", case.bad)):
            for change in answers:
                ws = lab.stage(cid, solution=True)
                path = ws / change.path
                if isinstance(change, Edit):
                    text = path.read_text()
                    assert change.old in text, f"{cid}: {change.old!r} is not in the reference {change.path}"
                    path.write_text(text.replace(change.old, change.new))
                elif isinstance(change, Write):
                    path.write_text(change.text)
                res = lab.check(ws)
                passed = res.ok if n is None else res.task_passes(n)
                if passed != (want == "ok"):
                    problems.append(("should pass" if want == "ok" else "should fail") + " | " + describe(cid, n, change, res))
    assert not problems, "\n\n".join(problems)


@pytest.mark.parametrize("cid", sorted(FLAGS))
def test_flag_hunts(lab, cid):
    ws = lab.stage(cid, solution=False)
    out = lab.sh(ws, f"bash {lab.folder(cid) / 'solution' / 'solve.sh'}").stdout.strip().splitlines()
    flag = out[-1].strip()
    case = FLAGS[cid]
    for text in case.ok:
        assert lab.engine.submit(cid, text.replace("{flag}", flag)), f"{cid} should accept {text!r}"
    for text in case.bad:
        assert not lab.engine.submit(cid, text.replace("{flag}", flag)), f"{cid} should reject {text!r}"
