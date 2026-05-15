from __future__ import annotations

import re

from .contract import load_contract
from .common import DelegateError


def _normalize_heading(value: str) -> str:
    value = value.strip().strip("#").strip().rstrip(":").strip().lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _present_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        if clean.startswith(("-", "*", ">")):
            continue
        if len(clean) > 80:
            continue
        headings.add(_normalize_heading(clean))
    return headings


def validate_task_file_contract(text: str) -> None:
    task_file = load_contract().get("taskFile", {})
    required = list(task_file.get("requiredSections") or [])
    aliases = task_file.get("sectionAliases") if isinstance(task_file.get("sectionAliases"), dict) else {}
    present = _present_headings(text)
    missing: list[str] = []
    for section in required:
        candidates = aliases.get(section) if isinstance(aliases.get(section), list) else [section]
        normalized = {_normalize_heading(str(candidate)) for candidate in candidates}
        if not present.intersection(normalized):
            missing.append(str(section))
    if missing:
        raise DelegateError("Task file contract failed. Missing required sections: " + ", ".join(missing) + ".")
