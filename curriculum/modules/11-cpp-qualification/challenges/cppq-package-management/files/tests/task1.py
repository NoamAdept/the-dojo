# Task 1: vcpkg.json manifest
import json, sys
try:
    m = json.load(open("vcpkg.json"))
except FileNotFoundError:
    sys.exit("create vcpkg.json")
except json.JSONDecodeError as e:
    sys.exit(f"vcpkg.json is not valid JSON: {e}")
assert m.get("name") == "pi-receiver" and m.get("version") == "0.1.0", "name/version"
deps = [d for d in m.get("dependencies", []) if isinstance(d, dict) and d.get("name") == "nlohmann-json"]
assert deps and deps[0].get("version>=") == "3.11.2", 'add {"name": "nlohmann-json", "version>=": "3.11.2"}'
