"""Consistency checks for the course data: schedule, backlog, and milestones."""

from __future__ import annotations

import datetime as dt
import re

import pytest

from backlog import (
    BASES,
    KINDS,
    PRIORITIES,
    RULE_STATUSES,
    load_backlog,
    load_milestones,
    load_schedule,
)

BACKLOG = load_backlog()
ITEMS = BACKLOG.by_id()
MILESTONES = {m["id"]: m for m in load_milestones()}
CHILDREN = [item for item in BACKLOG.items if item["kind"] != "epic"]


def minutes(value: str) -> int:
    hours, mins = value.split(":")
    return int(hours) * 60 + int(mins)


# ------------------------------------------------------------------ schedule


def test_schedule_fills_exactly_240_minutes_without_gaps() -> None:
    schedule = load_schedule()
    blocks = schedule["blocks"]
    assert blocks[0]["start"] == schedule["start"] == "09:00"
    assert blocks[-1]["end"] == schedule["end"] == "13:00"
    for before, after in zip(blocks, blocks[1:], strict=False):
        assert before["end"] == after["start"], f"gap or overlap at {after['start']}"
    total = sum(minutes(b["end"]) - minutes(b["start"]) for b in blocks)
    assert total == schedule["total_minutes"] == 240


def test_schedule_has_20_minutes_of_breaks_and_six_exercises() -> None:
    blocks = load_schedule()["blocks"]
    breaks = sum(
        minutes(b["end"]) - minutes(b["start"]) for b in blocks if b["kind"] == "break"
    )
    assert breaks == 20
    exercises = [b["id"] for b in blocks if b["kind"] == "exercise"]
    assert exercises == ["X1", "X2", "X3", "X4", "X5", "X6"]


# ------------------------------------------------------------------- backlog


def test_backlog_has_eight_epics_with_about_four_children() -> None:
    epics = [e["id"] for e in BACKLOG.epics()]
    assert epics == [f"E{n:02d}" for n in range(1, 9)]
    for epic in epics:
        assert 3 <= len(BACKLOG.children(epic)) <= 5, epic


def test_ids_are_unique_and_follow_the_pattern() -> None:
    ids = [item["id"] for item in BACKLOG.items]
    assert len(ids) == len(set(ids))
    for item in BACKLOG.items:
        if item["kind"] == "epic":
            assert re.fullmatch(r"E\d{2}", item["id"])
            assert "parent" not in item
        else:
            assert re.fullmatch(rf"{item['parent']}-[TS]\d", item["id"])


@pytest.mark.parametrize("item", CHILDREN, ids=lambda i: i["id"])
def test_child_has_required_fields(item: dict) -> None:
    assert item["kind"] in KINDS
    assert ITEMS[item["parent"]]["kind"] == "epic"
    for field in ("title", "output", "owner", "evidence"):
        assert str(item.get(field, "")).strip(), field
    assert item["acceptance_criteria"], "acceptance criteria missing"
    assert item["basis"] in BASES
    assert item["priority"] in PRIORITIES
    assert isinstance(item["start"], dt.date)
    assert isinstance(item["target"], dt.date)
    assert item["start"] <= item["target"]


@pytest.mark.parametrize(
    "item", [i for i in CHILDREN if i["basis"] == "Rule"], ids=lambda i: i["id"]
)
def test_rule_items_are_sourced(item: dict) -> None:
    source = item["source"]
    assert source["id"] in BACKLOG.sources
    assert source["article"].startswith("Art.")
    assert isinstance(source["page"], int)
    assert item["status"] in RULE_STATUSES
    if item["status"] != "verified":
        assert item["status_note"].strip(), "unverified rule needs a status note"


def test_story_uses_the_user_story_form() -> None:
    stories = [i for i in CHILDREN if i["kind"] == "story"]
    assert stories
    for story in stories:
        text = " ".join(story["story"].split())
        assert re.fullmatch(r"As .+, I need .+, so that .+\.", text), text


def test_dependencies_exist_are_not_hierarchy_and_respect_dates() -> None:
    for item in CHILDREN:
        for blocker_id in item.get("blocked_by", []):
            blocker = ITEMS[blocker_id]
            assert blocker_id != item["id"]
            assert blocker["kind"] != "epic", "block on a sub-issue, not on an epic"
            assert blocker_id != item["parent"], "dependency is not parent-child"
            assert blocker["target"] <= item["start"], (
                f"{item['id']} starts before its blocker {blocker_id} ends"
            )


def test_dependencies_have_no_cycle() -> None:
    graph = {i["id"]: i.get("blocked_by", []) for i in CHILDREN}
    visiting: set[str] = set()
    done: set[str] = set()

    def visit(node: str) -> None:
        assert node not in visiting, f"cycle through {node}"
        if node in done:
            return
        visiting.add(node)
        for nxt in graph.get(node, []):
            visit(nxt)
        visiting.remove(node)
        done.add(node)

    for node in graph:
        visit(node)


def test_milestone_references_exist_and_dates_fit() -> None:
    for item in CHILDREN:
        if "milestone" in item:
            milestone = MILESTONES[item["milestone"]]
            assert item["target"] <= milestone["due"], item["id"]


def test_learner_subset_matches_the_minimum_deliverable() -> None:
    learner = [i for i in BACKLOG.items if i.get("learner")]
    epics = [i["id"] for i in learner if i["kind"] == "epic"]
    subs = [i for i in learner if i["kind"] != "epic"]
    assert epics == ["E01", "E08"]
    assert len(subs) == 6
    assert all(i["parent"] in epics for i in subs)
    assert sum(1 for i in subs if i["kind"] == "story") == 1
    learner_ids = {i["id"] for i in learner}
    deps = [(i["id"], b) for i in subs for b in i.get("blocked_by", [])]
    assert deps, "learners need at least one blocking dependency"
    assert all(b in learner_ids for _, b in deps)
    assert {i["milestone"] for i in subs} == set(MILESTONES)


# ---------------------------------------------------------------- milestones


def test_three_milestones_with_justified_and_labelled_dates() -> None:
    assert list(MILESTONES) == ["M1", "M2", "M3"]
    for milestone in MILESTONES.values():
        assert milestone["date_status"] in ("fictional-formal", "proposed")
        assert milestone["justification"].strip()


def test_fictional_dates_match_the_six_month_writing_period() -> None:
    dates = BACKLOG.meta["fictional_dates"]
    assert MILESTONES["M1"]["due"] == dates["registration"] == dt.date(2026, 12, 1)
    assert MILESTONES["M3"]["due"] == dates["submission"] == dt.date(2027, 6, 1)
    registration = MILESTONES["M1"]["due"]
    six_months_later = registration.replace(
        year=registration.year + (registration.month + 6 - 1) // 12,
        month=(registration.month + 6 - 1) % 12 + 1,
    )
    assert MILESTONES["M3"]["due"] == six_months_later
    assert MILESTONES["M1"]["date_status"] == "fictional-formal"
    assert MILESTONES["M3"]["date_status"] == "fictional-formal"
