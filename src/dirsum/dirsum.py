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


def colour_hash_str(digest: str) -> str:
    """
    Colourize a hex digest string.

    :param digest: A hex digest str
    :returns: `digest` with ANSI escape codes to add colour
    """
    seed = int(digest, base=16) % 256
    opposite_seed = (seed - 128) % 128
    return f"\033[38:5:{seed}m\033[48:5:{opposite_seed}:m{digest}\033[m"


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

    sums = []

    for file in files:
        sum = hashlib.md5(file.read_bytes(), usedforsecurity=False)
        if config.pretty:
            print(f"{file}: {colour_hash_str(sum.hexdigest())}")
        else:
            print(f"{file} {sum.hexdigest()}")
        sums.append(sum.hexdigest())
    if config.pretty:
        print(f"\nTOTAL {colour_hash_str(hashlib.md5(''.join(sums).encode('utf-8')).hexdigest())}")
    else:
        print(f"\nTOTAL {hashlib.md5(''.join(sums).encode('utf-8')).hexdigest()}")
