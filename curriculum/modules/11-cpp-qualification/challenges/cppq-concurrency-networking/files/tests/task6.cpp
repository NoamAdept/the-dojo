// Task 6: connect() based ping, localhost only
#include "check.h"
#include "tasks.h"
int main() {
    int srv = socket(AF_INET, SOCK_STREAM, 0);
    sockaddr_in a{};
    a.sin_family = AF_INET;
    a.sin_addr.s_addr = htonl(INADDR_LOOPBACK);
    a.sin_port = 0;  // any free port
    EXPECT(bind(srv, (sockaddr*)&a, sizeof a) == 0 && listen(srv, 4) == 0);
    socklen_t len = sizeof a;
    getsockname(srv, (sockaddr*)&a, &len);
    uint16_t open_port = ntohs(a.sin_port);
    EXPECT(ping("127.0.0.1", open_port));
    close(srv);
    EXPECT(!ping("127.0.0.1", open_port));
}
