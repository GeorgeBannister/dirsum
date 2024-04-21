from ..ignore import get_non_ignored_files, parse_ignore_file

from pathlib import Path

FILE = Path(__file__)
TEST_ROOT = FILE.parent
TEST_IGNORE = TEST_ROOT / ".containerignore"


def test_ignore():
    rules, inverted_rules = parse_ignore_file(TEST_IGNORE)
    non_ignored_files = set(get_non_ignored_files(TEST_ROOT, rules, inverted_rules))
    for file in non_ignored_files:
        print(file)

    good_files = set(
        [
            Path("dir1/dir2/y.x"),
            Path("test_ignore.py"),
            Path("dir1/y.x"),
            Path(".containerignore"),
        ]
    )
    assert non_ignored_files == good_files
