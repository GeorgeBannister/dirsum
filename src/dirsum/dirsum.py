#!/usr/bin/env python3

import argparse
import hashlib
from pathlib import Path
from dataclasses import dataclass
from dirsum.ignore import get_non_ignored_files, parse_ignore_file


@dataclass(frozen=True, slots=True)
class Config:
    ignorefile: Path | None
    pretty: bool


def parse_args() -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ignore", help="Path to ignorefile")
    parser.add_argument("-p", "--pretty", help="Show colourful output", action="store_true")
    args = parser.parse_args()
    ignore_file = Path(args.ignore) if args.ignore else None
    pretty = args.pretty
    return Config(ignorefile=ignore_file, pretty=pretty)


def main() -> None:
    config = parse_args()
    files = None

    if config.ignorefile:
        rules, inverted_rules = parse_ignore_file(config.ignorefile)
        files = get_non_ignored_files(Path.cwd(), rules, inverted_rules)
    else:
        files = list([x.relative_to(Path.cwd()) for x in Path.cwd().glob("**/*") if not x.is_dir()])
    files.sort()
    for file in files:
        sum = hashlib.md5(file.read_bytes(), usedforsecurity=False)
        print(f"{file}: {sum.hexdigest()}")
