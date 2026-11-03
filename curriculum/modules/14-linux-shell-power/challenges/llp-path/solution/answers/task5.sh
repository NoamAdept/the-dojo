#!/bin/bash
mkdir -p fake
printf '#!/bin/bash\necho 1999\n' > fake/date
chmod +x fake/date
PATH="$PWD/fake:$PATH" ./report.sh
