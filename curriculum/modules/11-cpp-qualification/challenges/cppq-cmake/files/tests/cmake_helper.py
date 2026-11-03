"""Shared helper: configure + build a CMake project in a temp dir; return the build dir."""
import os, shutil, subprocess, sys, tempfile

def build(src, *options, target=None):
    if not os.path.isfile(os.path.join(src, "CMakeLists.txt")):
        sys.exit(f"{src}/CMakeLists.txt does not exist yet")
    out = tempfile.mkdtemp(prefix="cmake-")
    conf = subprocess.run(["cmake", "-S", src, "-B", out, *options], capture_output=True, text=True)
    if conf.returncode:
        sys.exit("cmake configure failed: " + (conf.stderr.strip().splitlines() or ["?"])[-1])
    cmd = ["cmake", "--build", out] + (["--target", target] if target else [])
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode:
        errs = [l for l in (done.stdout + done.stderr).splitlines() if "rror" in l][:2]
        sys.exit("build failed: " + " | ".join(errs))
    return out

def run(path, *args):
    if not os.path.exists(path):
        sys.exit(f"expected program {os.path.basename(path)} was not built")
    return subprocess.run([path, *args], capture_output=True, text=True, check=True).stdout
