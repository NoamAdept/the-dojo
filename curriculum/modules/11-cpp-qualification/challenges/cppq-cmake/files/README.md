# CMake Build Systems

This challenge is about build files. Each `tests/taskN.py` uses CMake to configure and build one of the small projects in this folder. It works offline. You can do the tasks in any order.

## CMake Build Systems and Project Configuration

Welcome to Module 10! Until now, you worked with single files or simple compile commands.

Real C++ projects are bigger. They have hundreds of files, many libraries, and strict settings. You cannot compile them by hand (`g++ main.cpp utils.cpp ...`). It is too much work.

This is why we use **CMake**. CMake does not build your project itself. It *generates* (creates) the build files for you. Examples of build files are a Makefile or a Visual Studio Solution.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

Each folder under `projects/` already has its C++ source files. Write the missing `CMakeLists.txt` files.

1. **First CMake** (`projects/calculator`):
   - Require CMake 3.10.
   - Use `project(Calculator)`.
   - Build `run_calc` from `calc.cpp`.
2. **Adding files**: also compile `ui.cpp` and `history.cpp` into `run_calc`. When you run it, it prints `ui+history ok`.
3. **Require C++20**: set `CMAKE_CXX_STANDARD 20` and `CMAKE_CXX_STANDARD_REQUIRED ON`. `calc.cpp` uses a C++20 feature.
4. **Conditional build** (`projects/gui_option`):
   - Add `option(BUILD_GUI "Build the GUI" ON)`.
   - Put `add_subdirectory(gui)` inside an `if`.
   - `gui/CMakeLists.txt` is already written for you.
5. **Project structure** (`projects/Game`):
   - Build `GameExe` from `src/main.cpp`.
   - The headers are in `include/`.
   - Put the program in `bin/` inside the build folder (use `RUNTIME_OUTPUT_DIRECTORY`).
6. **Library builder** (`projects/physics`):
   - Build a STATIC library `PhysicsCore` from `physics.cpp`.
   - Build `SimApp` from `main.cpp` and link it to the library.
7. **External library** (`projects/threads`): use `find_package(Threads REQUIRED)`. Then link `Threads::Threads` to `MultithreadedApp`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
