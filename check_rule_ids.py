import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
import sys

def extract_rule_ids_from_file(content):
    ids = set()
    try:
        root = ET.fromstring(content)
        for rule in root.findall(".//rule"):
            rule_id = rule.get("id")
            if rule_id and rule_id.isdigit():
                ids.add(int(rule_id))
    except ET.ParseError:
        pass
    return ids

def get_ids_in_main():
    result = subprocess.run(["git", "ls-tree", "-r", "origin/main", "--name-only"], capture_output=True, text=True, check=True)
    xml_files = [f for f in result.stdout.splitlines() if f.startswith("rules/") and f.endswith(".xml")]

    ids = set()
    for path in xml_files:
        show = subprocess.run(["git", "show", f"origin/main:{path}"], capture_output=True, text=True)
        ids.update(extract_rule_ids_from_file(show.stdout))
    return ids

def get_ids_in_pr():
    ids = set()
    for path in Path("rules").glob("*.xml"):
        try:
            content = path.read_text()
            ids.update(extract_rule_ids_from_file(content))
        except Exception:
            continue
    return ids

def main():
    pr_ids = get_ids_in_pr()
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
    main_ids = get_ids_in_main()
    conflicts = pr_ids & main_ids

    if conflicts:
        print(f"❌ Conflicting rule IDs: {sorted(conflicts)}")
        sys.exit(1)
    else:
        print("✅ No rule ID conflicts.")

if __name__ == "__main__":
    main()
