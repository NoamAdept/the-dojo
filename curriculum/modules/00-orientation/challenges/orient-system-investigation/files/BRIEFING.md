# EchoRelay Incident

EchoRelay should answer PING on localhost. Its answer should contain a lab flag.

What goes wrong:
- verify fails
- connection refused
- permission denied when the worker reads the token
- wrong listen port

Fix the running system so that `./echorelay/verify.sh` passes.
Do not rewrite verify.sh. Make the service match the contract (what verify expects).
