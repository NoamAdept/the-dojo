// Task 7: toolchain argument
#include "check.h"
#include "tasks.h"
int main() {
    EXPECT(toolchainArg("/opt/vcpkg") == "-DCMAKE_TOOLCHAIN_FILE=/opt/vcpkg/scripts/buildsystems/vcpkg.cmake");
    EXPECT(toolchainArg("/opt/vcpkg/") == "-DCMAKE_TOOLCHAIN_FILE=/opt/vcpkg/scripts/buildsystems/vcpkg.cmake");
}
