#!/usr/bin/env python3
import csv
import json
import sys

def investigate(input_path, output_path):
    groups = {}
    with open(input_path, newline="") as f:
        for row in csv.DictReader(f):
            if row["status"] != "LOCKED":
                continue
            station = row["station"]
            if station not in groups:
                groups[station] = []
            groups[station].append(float(row["snr"]))

    result = {}
    for station, values in groups.items():
        if len(values) >= 3:
            result[station] = {
                "count": len(values),
                "average_snr": round(sum(values) / len(values), 1),
            }

    with open(output_path, "w") as f:
        json.dump(result, f, sort_keys=True, indent=2)

if __name__ == "__main__":
    investigate(sys.argv[1], sys.argv[2])
