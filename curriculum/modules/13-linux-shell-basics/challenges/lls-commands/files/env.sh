# Source me from this folder:  . ./env.sh
export DOJO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/dojo"
export PATH="$DOJO/bin:$PATH"
echo "DOJO is now $DOJO"
