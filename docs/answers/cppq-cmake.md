## CMake Build Systems

*cppq-cmake · medium*

**Goal.** Write five `CMakeLists.txt` files, one per folder under `projects/`, so each project configures and builds and its program prints the expected line. No C++ needs to change.

**You need to know.**

- `cmake_minimum_required`, `project`, `add_executable` (README first sections).
- `set(CMAKE_CXX_STANDARD 20)` plus `CMAKE_CXX_STANDARD_REQUIRED ON`.
- `option()`, `if()`, `add_subdirectory()`; `add_library(... STATIC ...)` and `target_link_libraries`.
- `find_package(Threads REQUIRED)` gives the imported target `Threads::Threads`.

**Walkthrough.**

1. Run `./check`. Each task builds its project in a temp folder with `cmake -S <project> -B <tmp>` and `cmake --build`. You can do the same by hand to see full errors:

   ```bash
   cmake -S projects/calculator -B /tmp/b && cmake --build /tmp/b && /tmp/b/run_calc
   ```

2. Tasks 1 to 3 all use `projects/calculator/CMakeLists.txt`. Write the whole file at once: `calc.cpp` calls `ui()` and `history()` and uses `consteval`, so it only links with all three sources and only compiles as C++20.

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(Calculator CXX)
   set(CMAKE_CXX_STANDARD 20)
   set(CMAKE_CXX_STANDARD_REQUIRED ON)
   add_executable(run_calc calc.cpp ui.cpp history.cpp)
   ```

   The test checks the text too: the version must be `3.10` and the project name `Calculator`. `run_calc` prints `ui+history ok`.

3. Task 4, conditional build (`projects/gui_option/CMakeLists.txt`). `gui/CMakeLists.txt` already defines `gui_app`; the option decides whether that folder is included. `core_app` builds the existing `main.cpp`.

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(GuiOption CXX)
   option(BUILD_GUI "Build the GUI" ON)
   add_executable(core_app main.cpp)
   if(BUILD_GUI)
     add_subdirectory(gui)
   endif()
   ```

   The test builds twice, once default (expects `gui/gui_app`) and once with `-DBUILD_GUI=OFF` (expects no `gui_app`).

4. Task 5, project structure (`projects/Game/CMakeLists.txt`). `main.cpp` includes `"game.h"` from `include/`, so add that folder to the include path, and send the binary to `build/bin/`.

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(Game CXX)
   add_executable(GameExe src/main.cpp)
   target_include_directories(GameExe PRIVATE include)
   set_target_properties(GameExe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
   ```

   `bin/GameExe` prints `Pi Invaders`.

5. Task 6, library builder (`projects/physics/CMakeLists.txt`). `STATIC` produces `libPhysicsCore.a`, which the test looks for. Linking makes the library's code part of `SimApp`.

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(Physics CXX)
   add_library(PhysicsCore STATIC physics.cpp)
   target_include_directories(PhysicsCore PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
   add_executable(SimApp main.cpp)
   target_link_libraries(SimApp PRIVATE PhysicsCore)
   ```

   `SimApp` prints `19.62`.

6. Task 7, external library (`projects/threads/CMakeLists.txt`). `find_package` locates the system thread library and `Threads::Threads` adds the right `-pthread` flags.

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(Threaded CXX)
   find_package(Threads REQUIRED)
   add_executable(MultithreadedApp main.cpp)
   target_link_libraries(MultithreadedApp PUBLIC Threads::Threads)
   ```

   It prints `thread result 7`.

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`. On a Pi this takes a minute or so because every task runs a fresh CMake configure.

**Common mistakes.**

- Naming the file `CMakelists.txt` or `cmakelists.txt`: CMake only reads `CMakeLists.txt` (capital C, M, L).
- Doing Task 1 with only `calc.cpp`: it fails with undefined `ui()` / `history()` and a `consteval` error until all three sources and C++20 are in.
- Putting `set(CMAKE_CXX_STANDARD 20)` after `add_executable`: it must come before the target is created to apply to it.
