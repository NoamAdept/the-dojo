# Package Management with vcpkg

`cppq-package-management` · Orange Belt

**Goal:** Write a `vcpkg.json` manifest and a `deps.cmake` snippet (tasks 1 and 2), then five offline C++ helpers in `tasks.h` that mimic what a package manager does: compare versions, parse a manifest and build the toolchain flag.

**File `deps.cmake`**

```cmake
find_package(nlohmann_json CONFIG REQUIRED)
target_link_libraries(app PRIVATE nlohmann_json::nlohmann_json)
```

**File `tasks.h`**

```cpp
#pragma once
#include <sstream>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

inline std::string trim(const std::string& s) {
    auto b = s.find_first_not_of(" \t\r\n"), e = s.find_last_not_of(" \t\r\n");
    return b == std::string::npos ? "" : s.substr(b, e - b + 1);
}

inline bool versionMatches(const std::string& requested, const std::string& installed) {
    return trim(requested) == trim(installed);
}

inline std::vector<std::string> mockInstall(const std::string& pkg) {
    return {"Computing installation plan...", "Done installing: " + pkg};
}

class SemVer {
public:
    explicit SemVer(const std::string& text) {
        char d1 = 0, d2 = 0;
        std::istringstream in(text);
        if (!(in >> major_ >> d1 >> minor_ >> d2 >> patch_) || d1 != '.' || d2 != '.' || !in.eof())
            throw std::invalid_argument("bad version: " + text);
    }
    bool operator<(const SemVer& o) const {
        return std::tie(major_, minor_, patch_) < std::tie(o.major_, o.minor_, o.patch_);
    }
    bool operator==(const SemVer& o) const {
        return std::tie(major_, minor_, patch_) == std::tie(o.major_, o.minor_, o.patch_);
    }

private:
    int major_ = 0, minor_ = 0, patch_ = 0;
};

inline std::vector<std::string> parseDependencies(const std::string& json) {
    std::vector<std::string> out;
    auto key = json.find("\"dependencies\"");
    if (key == std::string::npos) return out;
    auto open = json.find('[', key), close = json.find(']', open);
    if (open == std::string::npos || close == std::string::npos) return out;
    for (auto q = json.find('"', open); q < close; q = json.find('"', q + 1)) {
        auto end = json.find('"', q + 1);
        out.push_back(json.substr(q + 1, end - q - 1));
        q = end;
    }
    return out;
}

inline std::string toolchainArg(std::string vcpkgRoot) {
    while (!vcpkgRoot.empty() && vcpkgRoot.back() == '/') vcpkgRoot.pop_back();
    return "-DCMAKE_TOOLCHAIN_FILE=" + vcpkgRoot + "/scripts/buildsystems/vcpkg.cmake";
}
```

**File `vcpkg.json`**

```json
{
  "name": "pi-receiver",
  "version": "0.1.0",
  "dependencies": [
    { "name": "nlohmann-json", "version>=": "3.11.2" }
  ]
}
```

Run `./check`. It must print `CHECK_OK`. Then press **Mark as done**.
