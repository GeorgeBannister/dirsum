from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class IgnoreRule():
    inverted: bool
    pattern: str

def parse_ignore_file(ignore_file: Path) -> list[IgnoreRule]:
    pass
