---
title: Decisions
description: Decision records for this course repository and an example record for the fictional thesis.
---

This page records the decisions behind this course. Each record has a context, a decision, its consequences, and its source. The last section shows an example record for the fictional thesis, as learners write it in exercise [X6](../course/exercises/x6.qmd).

| ID              | Date       | Decision                                                           | Status   |
| --------------- | ---------- | ------------------------------------------------------------------ | -------- |
| [D-001](#d-001) | 2026-10-12 | Create the course repository from the template at commit `c6ec5bc` | Accepted |
| [D-002](#d-002) | 2026-10-12 | Remove template parts that the course does not use                 | Accepted |
| [D-003](#d-003) | 2026-10-12 | Use labels instead of Issue Types                                  | Accepted |
| [D-004](#d-004) | 2026-10-12 | Use only synthetic data; real theses default to private            | Accepted |
| [D-005](#d-005) | 2026-10-12 | Licence prose and data under CC BY 4.0, code under AGPL 3.0        | Proposed |
| [D-006](#d-006) | 2026-10-12 | Use fictional registration and submission dates                    | Accepted |
| [D-007](#d-007) | 2026-10-12 | Describe scan reuse, not copyright, in the dataset                 | Accepted |
| [D-008](#d-008) | 2026-10-12 | Generate pages from YAML instead of executing code                 | Accepted |
| [D-009](#d-009) | 2026-10-12 | Confirm room F 001; keep pass/fail unresolved                      | Accepted |

## D-001 Create the repository from the template at commit `c6ec5bc` {#d-001}

**Context.** `SPECS.md` §5 requires that the course repository is created from `maehr/open-research-data-template`. Learners start from the same template.

**Decision.** The repository was created with "Use this template" from commit [`c6ec5bc`](https://github.com/maehr/open-research-data-template/commit/c6ec5bc366c21029e908ad16d54fa0e2201f18ee) of 16 June 2026. The direct commits to `main` change only the README, the licence, and the community-health files. All other work arrives through one pull request.

**Consequences.** The course records the template revision. When the template changes, the instructor checks the exercises against the new revision before the next run.

**Source.** `SPECS.md` §5 and §6, step 1.

## D-002 Remove template parts that the course does not use {#d-002}

**Context.** The template supports R, Python, Codespaces, a showcase site, and many scaffolds. The course needs a Quarto site and a few Python scripts for the maintainer.

**Decision.** Remove the R stack, the dev container, the showcase site, the template maintenance files, the changelog workflow, and the unused scaffolds. Keep Python through uv for maintainer tooling only.

**Consequences.** CI runs faster and needs no R. Learners do not see these files, because they start from the original template.

**Source.** Maintainer approval of the implementation plan, 12 October 2026.

## D-003 Use labels instead of Issue Types {#d-003}

**Context.** GitHub Issue Types exist only for organisations. A learner works in a personal account.

**Decision.** Mark epics, tasks, and stories with the labels `kind:epic`, `kind:task`, and `kind:story`.

**Consequences.** Every learner can follow the exercises with a free personal account.

**Source.** `SPECS.md` §3. GitHub Docs: [Managing issue types in an organization](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization).

## D-004 Use only synthetic data; real theses default to private {#d-004}

**Context.** The exercise repositories are public by default in the workshop. A real thesis can contain personal data, unpublished results, or material with third-party rights.

**Decision.** The public exercise uses only the 30 synthetic records. For real thesis work, the course recommends a private repository and a private Project.

**Consequences.** No real personal or research data enter the public exercise. Exercise X1 includes a visibility check, and the closing block covers the transfer to a private thesis.

**Source.** `SPECS.md` §2.

## D-005 Licence prose and data under CC BY 4.0, code under AGPL 3.0 {#d-005}

**Context.** The template releases code under AGPL 3.0 and data under CC BY 4.0. The course adds original teaching prose and screenshots of the GitHub interface.

**Decision.** Original teaching prose and data use CC BY 4.0. Code derived from the template keeps AGPL 3.0. Third-party material keeps its own rights, as [NOTICE.md](../NOTICE.md) lists.

**Consequences.** Others can reuse and adapt the course with attribution. The screenshots are not under CC BY 4.0.

**Source.** `SPECS.md` §5 ("Proposed CC BY 4.0"). Status stays "Proposed" until the instructor confirms it.

## D-006 Use fictional registration and submission dates {#d-006}

**Context.** The real registration and submission dates come from the Dean's Office. They differ per student.

**Decision.** The workshop uses the fictional registration date 2026-12-01 and the fictional submission date 2027-06-01. The six-month gap follows the DH study plan, Art. 15 Abs. 4. Intermediate milestones are adjustable estimates.

**Consequences.** Every page labels these dates as fictional. Real dates stay unconfirmed.

**Source.** `SPECS.md` §3. [Studienplan Digital Humanities](https://www.dh.unibe.ch/unibe/portal/fak_historisch/fsuf/d_dh/content/e1644823/e1776786/e1776810/e1777708/Studienplan_DH_Master_Major_Minor_ger.pdf), Art. 15 Abs. 4, p. 5.

## D-007 Describe scan reuse, not copyright, in the dataset {#d-007}

**Context.** A copyright status for fictional 19th-century periodicals would be implausible. The X6 scenario needs a rights restriction.

**Decision.** The column `scan_reuse_status` describes the reuse terms that a fictional archive gives for its scans. Record SYN-P021 is `restricted`.

**Consequences.** The rights restriction in X6 applies to the scans. The CSV itself stays under CC BY 4.0.

**Source.** [Data dictionary](../documentation/data-dictionary.qmd).

## D-008 Generate pages from YAML instead of executing code {#d-008}

**Context.** The backlog, the milestones, and the schedule must exist once, as versioned text, and also appear on the website.

**Decision.** `src/render_pages.py` writes Markdown pages from the YAML files. The pages are committed. A test fails when they are stale.

**Consequences.** The site build needs only Quarto. No document executes code.

**Source.** `SPECS.md` §3 ("Persist the instructor's full example backlog in versioned text").

## D-009 Confirm room F 001; keep pass/fail unresolved {#d-009}

**Context.** `SPECS.md` §6 step 4 requires a confirmation of the room, the pass/fail arrangement, the audience mix, and the thesis regulations before release.

**Decision.** The instructor confirmed on 12 October 2026: the room is Seminarraum F 001; the audience is mostly DH Major students; the 2025 DH study plan and RSL Phil.-hist. 21 are the basis of the example; real thesis dates stay unconfirmed. The pass/fail arrangement is not yet confirmed.

**Consequences.** The pages no longer mark the room as unresolved. The pass/fail callout stays. Risks U-01 and U-03 are updated.

**Source.** Instructor confirmation in the implementation session, 12 October 2026.

## Example: decision record for the fictional thesis {#example}

This is the record that learners write in exercise X6. It belongs in the learner's own repository, not here.

```markdown
## D-T01 Two-week delay of the scans and a reuse restriction

- **Date:** 2026-10-16 (workshop; fictional)
- **Context:** The fictional archive delivers the scans two weeks late. It
  restricts reuse of the scans for record SYN-P021.
- **Decision:** Move the start and target dates of E08-S1 by two weeks.
  Keep milestone M3 (submission, 2027-06-01) unchanged. Add a task to exclude
  the SYN-P021 scans from the public release. The demo release is blocked by
  that task.
- **Consequences:** M2 still holds. The release contains no SYN-P021 scans.
- **Not changed:** The official submission date. Only the supervisor can
  extend it (RSL Phil.-hist. 21 Art. 56 Abs. 2).
- **Links:** #<Issue number of E08-S1>, #<Issue number of the new task>
```
