---
title: Thesis documentation template
description: A reusable documentation template and issue forms for a master's thesis managed with GitHub.
---

This folder holds a documentation template for a master's thesis. It is a worked example from the workshop "GitHub as a Project Management Tool".

::: {.callout-important}
This template is **not** a thesis-format template that the University of Bern approved. It does not replace the rules of your study programme, the instructions of your supervisor, or the documents of the Dean's Office.
:::

## Files

| File                                                 | Use it for                                                                                                                                |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [`thesis-documentation.md`](thesis-documentation.md) | The documentation of the thesis project: question, scope, provenance, method, decisions, results, limits, rights, reproducibility, access |
| [`decision-record.md`](decision-record.md)           | One decision: context, decision, consequences, what did not change                                                                        |
| [`issue-forms/epic.yml`](issue-forms/epic.yml)       | An issue form for an epic                                                                                                                 |
| [`issue-forms/task.yml`](issue-forms/task.yml)       | An issue form for a task with output, owner, acceptance criteria, evidence, and basis                                                     |
| [`issue-forms/story.yml`](issue-forms/story.yml)     | An issue form for a user story                                                                                                            |

## How to use it

1. Create a **private** repository from the [open research data template](https://github.com/new?template_name=open-research-data-template&template_owner=maehr).
2. Copy `thesis-documentation.md` into `documentation/` and fill it in step by step. Leave a section empty with the note "not yet decided" instead of guessing.
3. Copy `decision-record.md` into `project-management/` for each important decision, or keep all decisions in one file `project-management/decisions.md`.
4. Copy the three issue forms into `.github/ISSUE_TEMPLATE/`. GitHub then offers them under **New issue**.

## Licence

CC BY 4.0. Reuse and adapt it with attribution to the course.
