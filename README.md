# GitHub as a Project Management Tool

A workshop and open educational resource (OER) with a browser route and a command-line route for each exercise. Learners plan, conduct, document, and share a fictional master's thesis with one GitHub repository and one GitHub Project.

[![GitHub issues](https://img.shields.io/github/issues/maehr/github-as-a-project-management-tool.svg)](https://github.com/maehr/github-as-a-project-management-tool/issues)
[![Prose licence](https://img.shields.io/badge/prose-CC%20BY%204.0-lightgrey.svg)](LICENSE-CCBY.md)
[![Code licence](https://img.shields.io/badge/code-AGPL%203.0-blue.svg)](LICENSE-AGPL.md)

> [!NOTE]
> **Status:** version [0.1.0](CHANGELOG.md) is the version taught on 16 October 2026 (tag `v0.1.0`). `main` holds the revision after the session: X1–X4 form the core workshop, and X5–X6 are optional extensions ([#17](https://github.com/maehr/github-as-a-project-management-tool/issues/17)). Website: <https://maehr.github.io/github-as-a-project-management-tool/>

**Worked example:** the [showcase Project](https://github.com/users/maehr/projects/11) holds the full plan of the fictional thesis, with its Issues in [`maehr/projm-example-thesis`](https://github.com/maehr/projm-example-thesis). It is linked to this repository's **Projects** tab.

## Course At A Glance

| Item     | Value                                                         |
| -------- | ------------------------------------------------------------- |
| Course   | `[PROJM] Github as a project management tool`, 526141, HS2026 |
| Type     | Workshop, Digital Humanities, University of Bern              |
| Lecturer | Dr. Moritz Mähr                                               |
| Date     | Friday, 16 October 2026, 09:00–13:00 (240 minutes)            |
| Room     | Seminarraum F 001, Hörraumgebäude Unitobler                   |
| Credits  | 0.5 ECTS, passed or failed                                    |

Details and registration: [KSL course entry](https://www.ksl.unibe.ch/KSL/kurzansicht?stammNr=526141&semester=HS2026&lfdNr=0).

## What Learners Do

Each learner works in the browser, on the command line with git and gh, or both. The browser route needs no software installation. Learners new to GitHub start with the [cheat sheet](course/cheat-sheet.qmd).

1. Create a repository from the [open research data template](https://github.com/new?template_name=open-research-data-template&template_owner=maehr).
2. Turn requirements into Issues, sub-issues, milestones, and dependencies.
3. Plan the work in a GitHub Project with a backlog, a board, and a roadmap.
4. Complete one documentation task through a pull request.
5. Decide what to publish, and prepare a demo release.
6. React to a delay and a rights restriction, choose one option, and record the decision.

The public exercise uses only synthetic data. For real thesis work, use a private repository and a private Project.

## Repository Structure

| Path                       | Content                                                             |
| -------------------------- | ------------------------------------------------------------------- |
| `course/`                  | Setup, syllabus, exercises X1–X6, solutions, instructor notes       |
| `slides/`                  | Reveal.js slides for the session                                    |
| `documentation/`           | Worked example, requirements register, publication note             |
| `project-management/`      | Seed source of the example backlog and milestones, decisions, risks |
| `archive/`                 | Pages that the site no longer shows; not rendered                   |
| `data/`                    | Synthetic periodical metadata for the exercises                     |
| `templates/master-thesis/` | Reusable thesis documentation template and issue forms              |
| `assets/screenshots/`      | Annotated screenshots of the GitHub interface and their sources     |
| `src/`, `test/`            | Maintainer scripts and checks; learners do not need them            |

## Maintain The Course

Maintainers need Node.js, uv, and Quarto 1.10.19. Learners need a browser, and git and gh for the command-line route.

| Task                                     | Command                                    |
| ---------------------------------------- | ------------------------------------------ |
| Run all checks                           | `npm run check`                            |
| Preview the site                         | `npm run preview`                          |
| Regenerate backlog and schedule pages    | `npm run pages:render`                     |
| Regenerate the synthetic CSV             | `npm run data:generate`                    |
| Annotate screenshots from raw captures   | `npm run screenshots:annotate`             |
| Seed the example backlog (dry run first) | `uv run python src/seed_backlog.py --help` |

## Provenance

This repository was created from [`maehr/open-research-data-template`](https://github.com/maehr/open-research-data-template) at commit [`c6ec5bc`](https://github.com/maehr/open-research-data-template/commit/c6ec5bc366c21029e908ad16d54fa0e2201f18ee) (16 June 2026). Learners start from that template, not from a fork of this course.

This course is an OER and a worked documentation example. It is not a thesis-format template that the university approved.

## Citation

Cite this course with the metadata in [CITATION.cff](CITATION.cff).

## Support

Use [GitHub Issues](https://github.com/maehr/github-as-a-project-management-tool/issues) to report an error in the course material. To report a security problem, read [SECURITY.md](SECURITY.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md) and the [code of conduct](CODE_OF_CONDUCT.md) before you open a pull request.

## Author

- **Moritz Mähr**: [maehr](https://github.com/maehr), [ORCID 0000-0002-1367-1618](https://orcid.org/0000-0002-1367-1618)

## Licence

Original teaching prose and data are released under [CC BY 4.0](LICENSE-CCBY.md). Code is released under [AGPL 3.0](LICENSE-AGPL.md), because it derives from the AGPL-licensed template. Third-party material keeps its own rights. [NOTICE.md](NOTICE.md) lists that material.
