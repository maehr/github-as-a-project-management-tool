"""Checks for the synthetic data, generated pages, images, and privacy."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import pytest
import yaml

import generate_synthetic_periodicals as generator
import render_pages
from backlog import ROOT

CSV_FILE = ROOT / "data" / "synthetic-periodicals.csv"
DICTIONARY = ROOT / "documentation" / "data-dictionary.qmd"
SCREENSHOTS = ROOT / "assets" / "screenshots"
CONTENT_DIRS = ["course", "documentation", "project-management", "slides", "templates"]
CONTENT_ROOT_FILES = ["index.qmd", "README.md"]


def content_files() -> list[Path]:
    files = [ROOT / "index.qmd", ROOT / "README.md"]
    for directory in CONTENT_DIRS:
        for pattern in ("*.qmd", "*.md", "*.yml"):
            files.extend((ROOT / directory).rglob(pattern))
    return sorted(p for p in files if p.exists())


def read_rows() -> list[dict[str, str]]:
    with CSV_FILE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


# ---------------------------------------------------------------- synthetic data


def test_csv_has_30_labelled_synthetic_records() -> None:
    rows = read_rows()
    assert len(rows) == 30
    ids = [row["record_id"] for row in rows]
    assert len(set(ids)) == 30
    assert all(re.fullmatch(r"SYN-P\d{3}", i) for i in ids)
    assert all(row["is_synthetic"] == "true" for row in rows)


def test_csv_matches_its_generator() -> None:
    assert read_rows() == generator.build_records()


def test_csv_columns_match_the_data_dictionary() -> None:
    text = DICTIONARY.read_text(encoding="utf-8")
    columns_section = text.split("\n## Columns\n", 1)[1].split("\n## ", 1)[0]
    documented = re.findall(r"^\| `([a-z_]+)` +\|", columns_section, flags=re.MULTILINE)
    with CSV_FILE.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    assert documented == header == generator.COLUMNS


# ---------------------------------------------------------------- generated pages


def test_generated_pages_are_current() -> None:
    for path, expected in render_pages.outputs().items():
        actual = path.read_text(encoding="utf-8")
        assert actual == expected, f"{path.name} is stale: run `npm run pages:render`"


# ---------------------------------------------------------------- images

IMAGE = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<src>[^)\s]+)")


def image_references() -> list[tuple[Path, str, str]]:
    refs = []
    for path in content_files():
        if path.suffix == ".yml":
            continue
        for match in IMAGE.finditer(path.read_text(encoding="utf-8")):
            refs.append((path, match["alt"], match["src"]))
    return refs


def test_every_image_exists_and_has_alt_text() -> None:
    for path, alt, src in image_references():
        if src.startswith("http"):
            continue
        assert alt.strip(), f"{path.relative_to(ROOT)}: image {src} has no alt text"
        assert (path.parent / src).resolve().exists(), f"missing image {src}"


SHORTCODE = re.compile(r"\{\{< screenshot (?P<name>[a-z0-9-]+) >\}\}")


def test_every_screenshot_is_annotated_used_and_present() -> None:
    annotations = yaml.safe_load((SCREENSHOTS / "annotations.yml").read_text())
    by_name = {
        shot["file"].removesuffix(".webp"): shot for shot in annotations["screenshots"]
    }
    used = {
        match["name"]
        for path in content_files()
        for match in SHORTCODE.finditer(path.read_text(encoding="utf-8"))
    }
    assert used <= set(by_name), f"unknown screenshots: {used - set(by_name)}"
    for name, shot in by_name.items():
        assert (SCREENSHOTS / shot["file"]).exists(), f"{shot['file']} not rendered"
        assert shot["alt"].strip(), f"{name} has no alt text"
        assert shot["callouts"], f"{name} has no callouts"
        assert name in used, f"{name} is not used on any page"
    files = {p.name for p in SCREENSHOTS.glob("*.webp")}
    assert files == {s["file"] for s in by_name.values()}, "unannotated image files"


# ---------------------------------------------------------------- privacy

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}")
ALLOWED_EMAILS = {"noreply@anthropic.com", "noreply@github.com"}


@pytest.mark.parametrize(
    "path", content_files(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_content_contains_no_email_address(path: Path) -> None:
    found = set(EMAIL.findall(path.read_text(encoding="utf-8"))) - ALLOWED_EMAILS
    found = {e for e in found if not e.endswith(("example.org", "example.com"))}
    assert not found, f"e-mail address in {path.relative_to(ROOT)}: {found}"
