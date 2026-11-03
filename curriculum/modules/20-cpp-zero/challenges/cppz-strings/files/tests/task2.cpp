// Task 2: countChar
#include "check.h"
#include "explain.h"
#include "tasks.h"
int main() {
    int n = countChar("mississippi", 's');
    SAY(n == 4, "countChar(\"mississippi\", 's') should be 4 but was " << n);
    n = countChar("radio", 'z');
    SAY(n == 0, "countChar(\"radio\", 'z') should be 0 but was " << n);
    n = countChar("", 'a');
    SAY(n == 0, "countChar of empty text should be 0 but was " << n);
}
