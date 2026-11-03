## Package Management with vcpkg

*cppq-package-management · medium*

**Goal.** Write a `vcpkg.json` manifest and a `deps.cmake` snippet (tasks 1 and 2), then five offline C++ helpers in `tasks.h` that mimic what a package manager does: compare versions, parse a manifest and build the toolchain flag.

**You need to know.**

- A vcpkg manifest is JSON with `name`, `version` and `dependencies` (README manifest section).
- `find_package(<pkg> CONFIG REQUIRED)` plus `target_link_libraries` with the imported target.
- `find_first_not_of` / `find_last_not_of` for trimming; `std::tie` for comparing several fields.
- Nothing is downloaded. The tests only read your files.

**Walkthrough.**

1. Run `./check`. Tasks 1 and 2 are Python tests that look for two new files in the challenge folder (next to `tasks.h`).

2. Task 1, create `vcpkg.json`. It must be valid JSON, and the version constraint key is literally `"version>="`.

   ```json
   {
     "name": "pi-receiver",
     "version": "0.1.0",
     "dependencies": [
       { "name": "nlohmann-json", "version>=": "3.11.2" }
     ]
   }
   ```

3. Task 2, create `deps.cmake`. Note the two spellings: the vcpkg port is `nlohmann-json`, but the CMake package is `nlohmann_json`.

   ```cmake
   find_package(nlohmann_json CONFIG REQUIRED)
   target_link_libraries(app PRIVATE nlohmann_json::nlohmann_json)
   ```

4. Task 3, version check. Trim spaces and newlines from both sides, then compare. The test passes `" 3.11.2\n"`.

   ```cpp
   inline std::string trim(const std::string& s) {
       auto b = s.find_first_not_of(" \t\r\n"), e = s.find_last_not_of(" \t\r\n");
       return b == std::string::npos ? "" : s.substr(b, e - b + 1);
   }
   inline bool versionMatches(const std::string& requested, const std::string& installed) {
       return trim(requested) == trim(installed);
   }
   ```

5. Task 4, mock install.

   ```cpp
   inline std::vector<std::string> mockInstall(const std::string& pkg) {
       return {"Computing installation plan...", "Done installing: " + pkg};
   }
   ```

6. Task 5, SemVer. Read `int . int . int` from a stream; anything else (like `1.x.3`) throws. `std::tie` compares major, then minor, then patch, as numbers, so `1.10.0` beats `1.9.9`. Add `#include <sstream>` and `#include <tuple>`.

   ```cpp
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
   ```

7. Task 6, manifest parser. Find `"dependencies"`, then its `[` and `]`, and collect every quoted string between them. Return an empty list if the key is missing.

   ```cpp
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
   ```

8. Task 7, toolchain path. Strip trailing slashes first so the result never has `//`.

   ```cpp
   inline std::string toolchainArg(std::string vcpkgRoot) {
       while (!vcpkgRoot.empty() && vcpkgRoot.back() == '/') vcpkgRoot.pop_back();
       return "-DCMAKE_TOOLCHAIN_FILE=" + vcpkgRoot + "/scripts/buildsystems/vcpkg.cmake";
   }
   ```

**Check.** `./check` prints `7/7 tasks pass` and `CHECK_OK`.

**Common mistakes.**

- Writing `nlohmann-json` in `deps.cmake` or `nlohmann_json` in `vcpkg.json`: each file uses its own spelling.
- Comparing versions as strings, so `"1.10.0" < "1.9.9"` comes out true.
- Putting `vcpkg.json` or `deps.cmake` in a subfolder: the tests open them from the challenge folder.
