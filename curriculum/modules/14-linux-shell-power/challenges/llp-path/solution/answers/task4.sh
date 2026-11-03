#!/bin/bash
mkdir -p "$HOME/bin"
printf '#!/bin/bash\necho "hello from pi"\n' > "$HOME/bin/hello-pi"
chmod +x "$HOME/bin/hello-pi"
echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
export PATH="$HOME/bin:$PATH"
hello-pi
