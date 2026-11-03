"""Python from Zero 09: a command-line program.

Usage: python3 report.py readings.txt   (writes report.txt)
"""
import sys


def read_lines(path):
    lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines


def write_lines(path, lines):
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def parse_reading(line):
    if "," not in line:
        raise ValueError(f"bad reading line: {line!r}")
    parts = line.split(",", 1)
    return [parts[0].strip(), int(parts[1])]


def best_snr(lines):
    best = {}
    for line in lines:
        name, snr = parse_reading(line)
        if name not in best or snr > best[name]:
            best[name] = snr
    return best


def report_lines(best):
    return [f"{name}: {best[name]}" for name in sorted(best)]


def main(path):
    write_lines("report.txt", report_lines(best_snr(read_lines(path))))


if __name__ == "__main__":
    main(sys.argv[1])
