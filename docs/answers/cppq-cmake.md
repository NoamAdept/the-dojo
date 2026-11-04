# CMake Build Systems

`cppq-cmake` · Orange Belt

**Goal:** Write five `CMakeLists.txt` files, one per folder under `projects/`, so each project configures and builds and its program prints the expected line. No C++ needs to change.

**File `projects/Game/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.10)
project(Game CXX)
add_executable(GameExe src/main.cpp)
target_include_directories(GameExe PRIVATE include)
set_target_properties(GameExe PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
```

**File `projects/calculator/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.10)
project(Calculator CXX)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
add_executable(run_calc calc.cpp ui.cpp history.cpp)
```

**File `projects/gui_option/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.10)
project(GuiOption CXX)
option(BUILD_GUI "Build the GUI" ON)
add_executable(core_app main.cpp)
if(BUILD_GUI)
  add_subdirectory(gui)
endif()
```

**File `projects/physics/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.10)
project(Physics CXX)
add_library(PhysicsCore STATIC physics.cpp)
target_include_directories(PhysicsCore PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
add_executable(SimApp main.cpp)
target_link_libraries(SimApp PRIVATE PhysicsCore)
```

**File `projects/threads/CMakeLists.txt`**

```cmake
cmake_minimum_required(VERSION 3.10)
project(Threaded CXX)
find_package(Threads REQUIRED)
add_executable(MultithreadedApp main.cpp)
target_link_libraries(MultithreadedApp PUBLIC Threads::Threads)
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
