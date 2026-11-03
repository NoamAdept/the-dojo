# Task 4: BUILD_GUI option controls the gui subdirectory
import os, sys
from cmake_helper import build
on = build("projects/gui_option")
off = build("projects/gui_option", "-DBUILD_GUI=OFF")
if not os.path.exists(os.path.join(on, "gui", "gui_app")):
    sys.exit("with BUILD_GUI=ON (the default) gui/gui_app should be built")
if os.path.exists(os.path.join(off, "gui", "gui_app")):
    sys.exit("with -DBUILD_GUI=OFF the gui must not be built")
