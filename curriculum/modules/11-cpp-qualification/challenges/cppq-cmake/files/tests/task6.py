# Task 6: static library PhysicsCore linked into SimApp
import glob, os, sys
from cmake_helper import build, run
out = build("projects/physics")
if not glob.glob(os.path.join(out, "**", "libPhysicsCore.a"), recursive=True):
    sys.exit("build PhysicsCore as a STATIC library (libPhysicsCore.a)")
assert run(os.path.join(out, "SimApp")).strip() == "19.62"
