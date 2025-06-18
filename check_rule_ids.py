import os
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

def extract_rule_ids(directory: Path):
    ids = set()
    for file in directory.glob("*.xml"):
        try:
            tree = ET.parse(file)
            root = tree.getroot()
            for rule in root.findall(".//rule"):
                rule_id = rule.get("id")
                if rule_id and rule_id.isdigit():
                    ids.add(int(rule_id))
        except ET.ParseError as e:
            print(f"⚠️ Skipping {file.name}: {e}")
    return ids

def main():
    pr_rules_dir = Path("rules")
    main_rules_dir = Path("main_branch/rules")

    if not pr_rules_dir.exists() or not main_rules_dir.exists():
        print("❌ Missing rules directory in one or both branches.")
        sys.exit(1)

    pr_ids = extract_rule_ids(pr_rules_dir)
    main_ids = extract_rule_ids(main_rules_dir)

    conflicts = pr_ids.intersection(main_ids)
    if conflicts:
        print(f"❌ Conflict: these rule IDs already exist in main: {sorted(conflicts)}")
        sys.exit(1)
    else:
        print("✅ No rule ID conflicts found.")

if __name__ == "__main__":
    main()
