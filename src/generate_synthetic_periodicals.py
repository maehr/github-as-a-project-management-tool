"""Generate the synthetic periodical metadata used in the course exercises.

Every record is invented. Titles combine word parts that were chosen to avoid
real periodical names. Places are generic Swiss towns. The fixed seed makes the
output reproducible, so the CSV in ``data/`` can be checked against this script.

Run with ``npm run data:generate``.
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

SEED = 2026
RECORD_COUNT = 30
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "synthetic-periodicals.csv"

COLUMNS = [
    "record_id",
    "title",
    "language",
    "place_of_publication",
    "first_year",
    "last_year",
    "frequency",
    "subject",
    "publisher",
    "scan_reuse_status",
    "digitised",
    "is_synthetic",
]

TITLE_PARTS = {
    "de": (
        ["Laternen", "Uhrmacher", "Mühlen", "Brücken", "Nebel", "Schindel"],
        ["kurier", "bote", "anzeiger", "rundschau", "stimme", "chronik"],
    ),
    "fr": (
        ["Le Courrier", "La Gazette", "L'Écho", "La Feuille", "Le Messager"],
        ["des Lanternes", "du Moulin", "des Ponts", "de la Brume", "des Horlogers"],
    ),
    "it": (
        ["La Voce", "Il Corriere", "La Gazzetta"],
        ["delle Lanterne", "del Mulino", "dei Ponti"],
    ),
}
PLACES = {
    "de": ["Bern", "Basel", "Zürich", "Luzern", "St. Gallen", "Chur", "Biel/Bienne"],
    "fr": ["Genève", "Lausanne", "Neuchâtel", "Fribourg", "Biel/Bienne"],
    "it": ["Lugano", "Bellinzona", "Locarno"],
}
LANGUAGE_WEIGHTS = {"de": 16, "fr": 10, "it": 4}
FREQUENCIES = ["daily", "weekly", "monthly", "quarterly", "irregular"]
SUBJECTS = ["politics", "culture", "religion", "economy", "science", "entertainment"]
PUBLISHER_STEMS = {
    "de": ["Druckerei", "Verlag"],
    "fr": ["Imprimerie", "Éditions"],
    "it": ["Tipografia", "Editrice"],
}
# Fictional reuse status of the scans, as a fictional holding archive states it.
REUSE_STATUS = ["open", "attribution-required", "unknown"]
GERMAN_ARTICLES = {"kurier": "Der", "bote": "Der", "anzeiger": "Der"}
DIGITISED = ["yes", "no", "partial"]

# Record numbers with a deliberate missing value. The data dictionary
# documents each case, so learners can describe missing values in X5.
MISSING_LAST_YEAR = {4, 11, 17, 23, 29}
MISSING_PUBLISHER = {8, 19, 26}
MISSING_FREQUENCY = {13, 27}
# Record with a fictional rights restriction for exercise X6.
RESTRICTED_RECORD = 21


def build_title(rng: random.Random, language: str, used: set[str]) -> str:
    first, second = TITLE_PARTS[language]
    while True:
        if language == "de":
            suffix = rng.choice(second)
            article = GERMAN_ARTICLES.get(suffix, "Die")
            title = f"{article} {rng.choice(first)}{suffix}"
        else:
            title = f"{rng.choice(first)} {rng.choice(second)}"
        if title not in used:
            used.add(title)
            return title


def build_records() -> list[dict[str, str]]:
    rng = random.Random(SEED)
    languages = [
        language for language, weight in LANGUAGE_WEIGHTS.items() for _ in range(weight)
    ]
    rng.shuffle(languages)
    used_titles: set[str] = set()
    records = []
    for number in range(1, RECORD_COUNT + 1):
        language = languages[number - 1]
        first_year = rng.randint(1830, 1905)
        last_year = first_year + rng.randint(2, 60)
        reuse = (
            "restricted" if number == RESTRICTED_RECORD else rng.choice(REUSE_STATUS)
        )
        place = rng.choice(PLACES[language])
        publisher = (
            f"{rng.choice(PUBLISHER_STEMS[language])} {place} No. {rng.randint(1, 9)}"
        )
        records.append(
            {
                "record_id": f"SYN-P{number:03d}",
                "title": build_title(rng, language, used_titles),
                "language": language,
                "place_of_publication": place,
                "first_year": str(first_year),
                "last_year": "" if number in MISSING_LAST_YEAR else str(last_year),
                "frequency": ""
                if number in MISSING_FREQUENCY
                else rng.choice(FREQUENCIES),
                "subject": rng.choice(SUBJECTS),
                "publisher": "" if number in MISSING_PUBLISHER else publisher,
                "scan_reuse_status": reuse,
                "digitised": rng.choice(DIGITISED),
                "is_synthetic": "true",
            }
        )
    return records


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(build_records())
    print(f"Wrote {RECORD_COUNT} synthetic records to {OUTPUT}")


if __name__ == "__main__":
    main()
