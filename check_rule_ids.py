import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import sys

def get_changed_rule_files():
    """Get a list of changed or added rule files in the PR."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        changed_files = [
            Path(f.strip()) for f in result.stdout.splitlines()
            if f.startswith("rules/") and f.endswith(".xml")
        ]
        return changed_files
    except subprocess.CalledProcessError as e:
        print("❌ Failed to get changed files:", e)
        sys.exit(1)

def extract_rule_ids_from_xml(content):
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

def get_rule_ids_in_files(files):
    ids = set()
    for path in files:
        try:
            content = path.read_text()
            ids.update(extract_rule_ids_from_xml(content))
        except Exception as e:
            print(f"⚠️ Could not read {path}: {e}")
    return ids

def get_all_main_rule_ids():
    """Get all rule IDs from the rules/*.xml files in origin/main."""
    subprocess.run(["git", "fetch", "origin", "main"], check=True)
    result = subprocess.run(
        ["git", "ls-tree", "-r", "origin/main", "--name-only"],
        capture_output=True,
        text=True,
        check=True,
    )
    xml_files = [
        f for f in result.stdout.splitlines()
        if f.startswith("rules/") and f.endswith(".xml")
    ]

    all_ids = set()
    for file in xml_files:
        show = subprocess.run(
            ["git", "show", f"origin/main:{file}"],
            capture_output=True,
            text=True,
        )
        all_ids.update(extract_rule_ids_from_xml(show.stdout))
    return all_ids

def main():
    changed_files = get_changed_rule_files()
    if not changed_files:
        print("✅ No rule files were changed in this PR.")
        return

    # print(f"🔍 Checking these files for conflicts: {[f.name for f in changed_files]}")

    # changed_ids = get_rule_ids_in_files(changed_files)
    # main_ids = get_all_main_rule_ids()
    # conflicts = changed_ids & main_ids

    # if conflicts:
    #     print(f"❌ Conflicting rule IDs: {sorted(conflicts)}")
    #     sys.exit(1)
    # else:
    #     print("✅ No rule ID conflicts.")

    print(f"🔍 Checking these files for conflicts: {[f.name for f in changed_files]}")
    main_ids = get_all_main_rule_ids()

    # Loop through each changed file and check for ID conflicts
    for path in changed_files:
        print(f"\n🔎 Checking file: {path.name}")
        try:
            content = path.read_text()
            file_ids = extract_rule_ids_from_xml(content)
        except Exception as e:
            print(f"⚠️ Could not read {path.name}: {e}")
            continue
        conflicts = file_ids & main_ids
        if conflicts:
            print(f"❌ Conflicting rule IDs in {path.name} file. Rule IDs: {sorted(conflicts)}")
            sys.exit(1)
        else:
            print(f"✅ No rule ID conflicts in {path.name}.")

    print("\n✅ All checked files are conflict-free.")

if __name__ == "__main__":
    main()
