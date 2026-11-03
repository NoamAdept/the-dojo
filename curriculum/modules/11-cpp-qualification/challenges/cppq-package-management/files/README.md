# Package Management with vcpkg

Write all your code in `tasks.h`. You can write inline, header-only code here. Each file in `tests/` checks one task. `./check` compiles them one at a time with `g++ -std=c++17`. So you can do the tasks in any order.

Tasks 1 and 2 are files, not C++: `vcpkg.json` and `deps.cmake`. vcpkg itself needs the internet. So nothing here installs packages.

## C++ Package Management with vcpkg

Welcome to Module 11! In this module, you learn about **Package Management** in C++. We use the tool **vcpkg**.

In the past, C++ had no standard package manager. People downloaded, built, and linked libraries by hand. Today, tools like **vcpkg** (from Microsoft) give a standard way to do this.

Is this new to you? Read **LESSON.md** first (or press **Lesson** in the app).

## Your tasks

1. **vcpkg.json**: write a manifest.
   - The name is `pi-receiver`.
   - The version is `0.1.0`.
   - It depends on `nlohmann-json` with `"version>=": "3.11.2"`.
2. **CMake logic**: in `deps.cmake`, write `find_package(nlohmann_json CONFIG REQUIRED)` and `target_link_libraries(app PRIVATE nlohmann_json::nlohmann_json)`.
3. **Version check**: `bool versionMatches(const std::string& requested, const std::string& installed)` returns true when they are equal. Remove the whitespace (spaces) at the start and end first.
4. **Mock install**: `std::vector<std::string> mockInstall(const std::string& pkg)` returns `{"Computing installation plan...", "Done installing: <pkg>"}`.
5. **SemVer**:
   - `SemVer(const std::string&)` reads `"X.Y.Z"`.
   - It throws `std::invalid_argument` when the input is bad.
   - Give it `operator<` and `operator==`.
   - Compare the parts as numbers, so that `1.10.0 > 1.9.9`.
6. **Manifest parser**: `std::vector<std::string> parseDependencies(const std::string& json)` returns the string entries from the `"dependencies"` array. Use plain string handling (no JSON library).
7. **Toolchain path**: `std::string toolchainArg(std::string vcpkgRoot)` returns `-DCMAKE_TOOLCHAIN_FILE=<root>/scripts/buildsystems/vcpkg.cmake`. If the root ends in `/`, do not add a second `/`.

## Check your work

Run `./check` as often as you like. It lists every task that still fails. When it prints `CHECK_OK`, press **Done** in the dojo.
