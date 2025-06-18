import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

def get_changed_xml_files():
    """Return a list of added or modified XML files in rules/ dir compared to main."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "origin/main...HEAD"],
        capture_output=True, text=True, check=True
    )
    files = [f.strip() for f in result.stdout.splitlines()]
    return [Path(f) for f in files if f.startswith("rules/") and f.endswith(".xml")]

def extract_rule_ids_from_file(file_path: Path):
    ids = set()
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for rule in root.findall(".//rule"):
            rule_id = rule.get("id")
            if rule_id and rule_id.isdigit():
                ids.add(int(rule_id))
    except ET.ParseError as e:
        print(f"⚠️ Skipping {file_path.name}: {e}")
    return ids

def extract_rule_ids_from_main():
    """Check out the main branch's rules/ and extract all rule IDs"""
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
    result = subprocess.run(["git", "ls-tree", "-r", "origin/main", "--name-only"], capture_output=True, text=True, check=True)
    xml_files = [f for f in result.stdout.splitlines() if f.startswith("rules/") and f.endswith(".xml")]

    ids = set()
    for file in xml_files:
        content = subprocess.run(["git", "show", f"origin/main:{file}"], capture_output=True, text=True)
        try:
            root = ET.fromstring(content.stdout)
            for rule in root.findall(".//rule"):
                rule_id = rule.get("id")
                if rule_id and rule_id.isdigit():
                    ids.add(int(rule_id))
        except ET.ParseError:
            print(f"⚠️ Failed to parse {file} from main branch.")
    return ids

def main():
    changed_files = get_changed_xml_files()
    if not changed_files:
        print("ℹ️ No rule files changed in this PR. Nothing to check.")
        return

    print(f"🔍 Checking changed rule files: {[f.name for f in changed_files]}")

    pr_rule_ids = set()
    for f in changed_files:
        pr_rule_ids.update(extract_rule_ids_from_file(f))

    main_rule_ids = extract_rule_ids_from_main()
    conflicts = pr_rule_ids.intersection(main_rule_ids)

    if conflicts:
        print(f"❌ Conflict: these rule IDs already exist in main: {sorted(conflicts)}")
        sys.exit(1)
    else:
        print("✅ No rule ID conflicts with main.")

if __name__ == "__main__":
    main()
