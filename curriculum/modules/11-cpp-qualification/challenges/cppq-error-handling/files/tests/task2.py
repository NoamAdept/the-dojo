# Task 2: [[nodiscard]] makes ignored results a warning
import os, subprocess, sys, tempfile
ok = os.path.join(tempfile.mkdtemp(), "ok.cpp")
open(ok, "w").write('#include "tasks.h"\nint main() { return square(3) == 9 ? 0 : 1; }\n')
bad = os.path.join(tempfile.mkdtemp(), "bad.cpp")
open(bad, "w").write('#include "tasks.h"\nint main() { square(3); }\n')
base = ["g++", "-std=c++17", "-I.", "-Werror", "-Wall", "-c", "-o", os.devnull]
if subprocess.run(base + [ok], capture_output=True).returncode:
    sys.exit("square(int) does not compile yet")
if subprocess.run(base + [bad], capture_output=True).returncode == 0:
    sys.exit("the compiler must warn when you ignore the result of square(). Mark it [[nodiscard]]")
