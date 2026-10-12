"""Load the example backlog and format Issue bodies.

The render script and the seed script share this module, so the handbook and
the instructor's example repository show the same text.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
BACKLOG_FILE = ROOT / "project-management" / "backlog.yml"
MILESTONES_FILE = ROOT / "project-management" / "milestones.yml"
SCHEDULE_FILE = ROOT / "course" / "schedule.yml"

KINDS = ("epic", "task", "story")
BASES = ("Rule", "Practice", "Demo")
RULE_STATUSES = ("verified", "unconfirmed", "fictional")
PRIORITIES = ("High", "Normal", "Low")


@dataclass(frozen=True)
class Backlog:
    meta: dict[str, Any]
    sources: dict[str, dict[str, Any]]
    labels: list[dict[str, str]]
    items: list[dict[str, Any]]

    def by_id(self) -> dict[str, dict[str, Any]]:
        return {item["id"]: item for item in self.items}

    def epics(self) -> list[dict[str, Any]]:
        return [item for item in self.items if item["kind"] == "epic"]

    def children(self, epic_id: str) -> list[dict[str, Any]]:
        return [item for item in self.items if item.get("parent") == epic_id]

    def epic_dates(self, epic_id: str) -> tuple[dt.date, dt.date]:
        kids = self.children(epic_id)
        return min(k["start"] for k in kids), max(k["target"] for k in kids)


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_backlog(path: Path = BACKLOG_FILE) -> Backlog:
    data = load_yaml(path)
    return Backlog(
        meta=data["meta"],
        sources=data["sources"],
        labels=data["labels"],
        items=data["items"],
    )


def load_milestones(path: Path = MILESTONES_FILE) -> list[dict[str, Any]]:
    return load_yaml(path)["milestones"]


def load_schedule(path: Path = SCHEDULE_FILE) -> dict[str, Any]:
    return load_yaml(path)


def issue_title(item: dict[str, Any]) -> str:
    return f"{item['id']} {item['title']}"


def basis_line(item: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    if item["basis"] != "Rule":
        return item["basis"]
    ref = item["source"]
    source = sources[ref["id"]]
    return (
        f"Rule: [{ref['id']}]({source['url']}) {ref['article']}, p. {ref['page']} "
        f"({item['status']})"
    )


def issue_body(item: dict[str, Any], backlog: Backlog) -> str:
    """Return the Markdown body for a GitHub Issue."""
    if item["kind"] == "epic":
        kids = backlog.children(item["id"])
        lines = [
            f"**Outcome:** {item['outcome']}",
            "",
            "**Sub-issues:** " + ", ".join(f"{k['id']} {k['title']}" for k in kids),
            "",
            "_Fictional thesis. Synthetic data only._",
        ]
        return "\n".join(lines)

    lines = []
    if item["kind"] == "story":
        lines += [f"> {item['story']}", ""]
    lines += [
        f"**Output:** {item['output']}",
        f"**Owner:** {item['owner']}",
        f"**Basis:** {basis_line(item, backlog.sources)}",
    ]
    if item.get("status_note"):
        lines.append(f"**Status note:** {item['status_note']}")
    lines += ["", "**Acceptance criteria**", ""]
    lines += [f"- [ ] {criterion}" for criterion in item["acceptance_criteria"]]
    lines += ["", f"**Evidence:** {item['evidence']}"]
    if item.get("blocked_by"):
        lines.append(f"**Blocked by:** {', '.join(item['blocked_by'])}")
    lines += ["", "_Fictional thesis. Synthetic data only._"]
    return "\n".join(lines)
