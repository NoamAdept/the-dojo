#!/usr/bin/env python3
import sys

def parse_config(path):
    """Return a dict from name=value lines; ignore blanks and # comments."""
    result = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue
            if "=" not in line:
                raise ValueError("line without '=': " + line)
            name, value = line.split("=", 1)
            result[name.strip()] = value.strip()
    return result

if __name__ == "__main__":
    config = parse_config(sys.argv[1])
    with open("parsed.txt", "w") as out:
        for key in sorted(config):
            out.write(f"{key}={config[key]}\n")
