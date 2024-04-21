from pathlib import Path

def parse_ignore_file(ignore_file: Path) -> tuple[list[str], list[str]]:
    normal_rules = []
    inverted_rules = []
    for line in ignore_file.read_text().splitlines():
        if not line or line[0] == '#':
            continue
        if line[0] == "!":
            inverted_rules.append(line[1:])
        else:
            normal_rules.append(line)
    return (normal_rules, inverted_rules)

def get_non_ignored_files(root: Path, normal_rules: list[str], inverted_rules: list[str]) -> list[Path]:
    assert root.exists() and root.is_dir(), "Bad root"
    safe_files = set([x for rule in inverted_rules for x in root.glob(rule)])
    matching_files = set([x for rule in normal_rules for x in root.glob(rule)])
    all_files = set(root.glob("**/*"))
    culled_files = (matching_files - safe_files)
    culled_children = set()
    for file in culled_files:
        if file.is_dir():
            for f in file.glob("**/*"):
                culled_children.add(f)
                
    return [x.relative_to(root) for x in all_files - culled_files - culled_children if not x.is_dir()]
