# CMake Build Systems: lesson

CMake is a tool that writes build files for you. You describe your project in a simple text file. CMake reads it and creates the real build files (for example a Makefile).

### 1. The `CMakeLists.txt` File

Every CMake project starts with a file in the root folder. Its name must be exactly `CMakeLists.txt`.

**Minimal Example:**

```cmake
cmake_minimum_required(VERSION 3.10)

## Name of the project
project(MyAwesomeProject)

## Tell CMake to create an executable named 'MyApp' from 'main.cpp'
add_executable(MyApp main.cpp)
```

- `cmake_minimum_required` says which CMake version you need, at least.
- `project` gives your project a name.
- `add_executable` makes a program (an executable) from source files.

### 2. Converting to a Build

To use this file, you usually run these commands in a terminal:

```bash
mkdir build        # Create a clean folder for build artifacts
cd build
cmake ..           # Read CMakeLists.txt from the parent directory and generate Makefile
make               # Read the Makefile and compile the code
```

This creates a program file named `MyApp` in the build folder.

Build artifacts are the files that the build creates. Keep them in a separate folder, so your source folder stays clean.

### 3. Multiple Source Files

Do you have `main.cpp` and `utils.cpp`? Then list both files:

```cmake
add_executable(MyApp main.cpp utils.cpp)
```

### 4. Using Variables

When you have many files, a variable makes the file easier to read. A variable is a name that holds a value. Here it holds a list of files.

```cmake
set(SOURCES
    main.cpp
    utils.cpp
    math_helpers.cpp
)

add_executable(MyApp ${SOURCES})
```

`${SOURCES}` means "the value of the variable `SOURCES`".

### 5. Include Directories

Sometimes your header files (`.h`) are in their own `include/` folder. Tell CMake where to look. Then `#include "header.h"` works without a full path.

```cmake
target_include_directories(MyApp PUBLIC ${CMAKE_SOURCE_DIR}/include)
```

### 6. Setting C++ Standard

A C++ standard is a version of the C++ language, for example C++17 or C++20. Modern C++ code needs a modern standard. Always say which standard you need.

```cmake
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
```

`CMAKE_CXX_STANDARD_REQUIRED` means: stop with an error if the compiler does not support this standard.

### 7. Libraries (Static)

A library is a group of compiled code that other programs can use. You can make your own libraries to organize your code.

A static library (`.a` / `.lib`) is linked at build time. This means its code is copied into your program when you build it.

```cmake
## Create a library named 'MathLib' from math.cpp
add_library(MathLib math.cpp)

## Link it to the executable
target_link_libraries(MyApp PUBLIC MathLib)
```

### 8. Subdirectories

Large projects usually have subfolders. Each subfolder has its own `CMakeLists.txt`. This keeps the build logic in small, separate parts (modular).

**Root CMakeLists.txt:**
```cmake
add_subdirectory(src)
add_subdirectory(tests)
```

### 9. `find_package`

Use `find_package` to use external libraries (like `boost` or `pthread`). An external library is one that is not part of your project. `find_package` looks for libraries that are installed on your system.

```cmake
find_package(Threads REQUIRED)

target_link_libraries(MyApp PUBLIC Threads::Threads)
```

`REQUIRED` means: stop with an error if CMake cannot find the library.

### 10. Cache Variables (`option`)

An `option` is a cache variable (a setting that CMake remembers between runs). Users can change it when they build your code. For example: `cmake -DENABLE_TESTS=OFF ..`.

```cmake
option(ENABLE_TESTS "Build tests" ON)

if(ENABLE_TESTS)
    add_subdirectory(tests)
endif()
```

Here the default is `ON`. With `-DENABLE_TESTS=OFF`, CMake skips the `tests` folder.

---

## New words

- **build files**: files that tell the compiler what to build and how (for example a Makefile).
- **target**: something CMake builds, such as a program or a library.
- **executable**: a program file that you can run.
- **static library**: compiled code that is copied into your program at build time.
- **cache variable**: a setting that CMake stores and remembers between runs.

## Offline help

- Offline: `man cmake`, `cmake --help-command add_executable`
