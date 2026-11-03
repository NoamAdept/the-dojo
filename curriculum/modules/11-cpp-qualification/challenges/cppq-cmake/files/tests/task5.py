# Task 5: Game layout, executable in bin/
import os
from cmake_helper import build, run
out = build("projects/Game")
assert run(os.path.join(out, "bin", "GameExe")).strip() == "Pi Invaders"
