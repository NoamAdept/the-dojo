"""Python from Zero 09: a command-line program.

Usage: python3 report.py readings.txt   (writes report.txt)
"""
import sys


def read_lines(path):
    """Done for you (from the last challenge)."""
    lines = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines


def write_lines(path, lines):
    """Done for you (from the last challenge)."""
    with open(path, "w") as f:
        for line in lines:
            f.write(line + "\n")


def parse_reading(line):
    """Task 1: "tower,12" -> ["tower", 12]; raise ValueError if there is no comma."""
    raise NotImplementedError


def best_snr(lines):
    """Task 2: {station: highest snr} from a list of "station,snr" lines."""
    raise NotImplementedError


def report_lines(best):
    """Task 3: ["station: snr", ...] sorted by station name."""
    raise NotImplementedError


def main(path):
    """Task 4: read path, compute best SNRs, write report.txt."""
    raise NotImplementedError


# Task 5: add the  if __name__ == "__main__":  block here.
