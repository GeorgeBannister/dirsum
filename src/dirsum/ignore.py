from pathlib import Path


def parse_ignore_file(ignore_file: Path) -> tuple[list[str], list[str]]:
    """
    Parse a `.containerignore` or similar for rules.

    :param ignore_file: `Path` to file to parse
    :returns: Tuple (list of ignore rules, list of exception rules)
    """
    normal_rules = []
    exception_rules = []
    for line in ignore_file.read_text().splitlines():
        if not line or line[0] == "#":
            continue
        if line[0] == "!":
            exception_rules.append(line[1:])
        else:
            normal_rules.append(line)
    return (normal_rules, exception_rules)


def get_non_ignored_files(root: Path, normal_rules: list[str], exception_rules: list[str]) -> list[Path]:
    """
    Take a root directory and ignore rules and return the list of non-ignored files.

    :param root: `Path` to root directory
    :normal_rules: List of ignore glob rules
    :exception_rules: List of exception glob rules
    :returns: List of non-ignored files
    """
    assert root.exists() and root.is_dir(), "Bad root"
    safe_files = set([x for rule in exception_rules for x in root.glob(rule)])
    matching_files = set([x for rule in normal_rules for x in root.glob(rule)])
    all_files = set(root.glob("**/*"))
    culled_files = matching_files - safe_files
    culled_children = set()
    for file in culled_files:
        if file.is_dir():
            for f in file.glob("**/*"):
                culled_children.add(f)
    return [x.relative_to(root) for x in all_files - culled_files - culled_children if not x.is_dir()]
