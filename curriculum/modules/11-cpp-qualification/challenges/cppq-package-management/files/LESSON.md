# Package Management with vcpkg: lesson

A package is a library that someone else wrote and that you want to use. A package manager is a tool that finds, builds and installs these libraries for you.

### 1. The Old Way vs. The New Way

#### The Old Way

- You download the source code by hand.
- You build each dependency, one at a time. (A dependency is a library that your project needs.)
- You set the include paths and linker flags by hand.

#### The New Way (vcpkg)

- You list your dependencies in a manifest file (`vcpkg.json`). A manifest is a file that describes your project.
- You run CMake and give it the vcpkg toolchain file.
- vcpkg downloads, compiles, and installs the dependencies for you.

### 2. Installing vcpkg

**vcpkg** is a package manager that you use from the command line. It works on many systems (it is cross-platform). To install it, you clone (copy) its repository, microsoft/vcpkg on GitHub. Then you run a bootstrap script (a small setup script). This needs internet, and this challenge does not need it: everything here works offline.

```bash
git clone <the microsoft/vcpkg repository>
./vcpkg/bootstrap-vcpkg.sh  # (or .bat on Windows)
```

```cpp
// Note: This cell simulates a terminal check
#include <iostream>
#include <cstdlib>

int main() {
    std::cout << "Checking vcpkg version..." << std::endl;
    // In a real shell: ./vcpkg/vcpkg --version
    std::system("echo 'vcpkg package management program version 2023-XX-XX'");
    return 0;
}
```

### 3. The `vcpkg.json` Manifest

In **Manifest Mode**, you list your project's dependencies in a `vcpkg.json` file. This file sits in the root folder of your project.

Here is an example `vcpkg.json` that uses the **fmt** library:

```json
{
  "name": "my-project",
  "version-string": "1.0.0",
  "dependencies": [
    "fmt"
  ]
}
```

### 4. Classic Mode vs. Manifest Mode

#### Classic Mode

You install libraries by hand for all your projects at once (for your user). You use `vcpkg install [package]`. You must look after the installed packages yourself.

#### Manifest Mode (Recommended)

Each project has its own dependencies, listed in `vcpkg.json`. When you configure your project, vcpkg installs them into a local `vcpkg_installed` folder.

### 5. Integrating with CMake

To use vcpkg with CMake, you must give CMake the **vcpkg toolchain file**. A toolchain file tells CMake extra settings, here: where vcpkg puts the packages.

```bash
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=[path-to-vcpkg]/scripts/buildsystems/vcpkg.cmake
```

Then use `find_package` in `CMakeLists.txt` as normal:

```cmake
find_package(fmt REQUIRED)
add_executable(my_app main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt)
```

```cpp
// Simulating code using 'fmt' installed via vcpkg
// #include <fmt/core.h>
#include <iostream>

int main() {
    // fmt::print("Hello, {}!\n", "vcpkg"); 
    std::cout << "Hello, vcpkg! (Standard output)" << std::endl;
    return 0;
}
```

### 6. Versioning and Overrides

Manifest mode supports **versioning**. You can ask for exact versions, or use baselines. A baseline is a fixed point in the vcpkg catalog. It decides which versions you get.

```json
{
  "dependencies": [
    { "name": "fmt", "version>=": "10.0.0" }
  ],
  "builtin-baseline": "[commit-sha]"
}
```

### 7. Custom Ports and Registries

Sometimes a library is not in the main vcpkg catalog. Then you have 2 choices:

- Create a **Custom Port**. This is a folder with a `portfile.cmake` file. The file tells vcpkg how to build the library.
- Use a separate **Registry** (another catalog of packages).

### 8. Best Practices

1. **Use Manifest Mode**: Always use `vcpkg.json`. Then every build uses the same packages (reproducible builds).
2. **Commit the Manifest**: Add `vcpkg.json` and `vcpkg-configuration.json` to git.
3. **Ignore `vcpkg_installed`**: Add `vcpkg_installed/` to your `.gitignore`.
4. **Use Baselines**: Update your baseline commit from time to time. This upgrades your dependencies.

---

## New words

- **package**: a library that you can install and use in your project.
- **dependency**: a library that your project needs.
- **manifest**: a file that lists your project's dependencies (`vcpkg.json`).
- **toolchain file**: a file that gives CMake extra settings.
- **baseline**: a fixed point in the vcpkg catalog that decides which versions you get.
- **semantic version (SemVer)**: a version number in the form `X.Y.Z` (major.minor.patch).
