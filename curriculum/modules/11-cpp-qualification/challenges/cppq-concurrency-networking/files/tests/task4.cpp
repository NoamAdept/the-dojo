// Task 4: sockaddr_in
#include "check.h"
#include "tasks.h"
int main() {
    sockaddr_in a = makeAddress("127.0.0.1", 8888);
    EXPECT(a.sin_family == AF_INET);
    EXPECT(ntohs(a.sin_port) == 8888);
    EXPECT(a.sin_addr.s_addr == htonl(INADDR_LOOPBACK));
}
