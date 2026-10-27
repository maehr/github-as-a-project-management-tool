---
title: Decisions
description: Decision records for this course repository.
---

This page records the decisions behind this course. Each record has a context, a decision, its consequences, and its source. For an example record of the fictional thesis, as learners write it in exercise X6, see [Solutions](../course/solutions.qmd#x6).

| ID              | Date       | Decision                                                            | Status              |
| --------------- | ---------- | ------------------------------------------------------------------- | ------------------- |
| [D-001](#d-001) | 2026-10-12 | Create the course repository from the template at commit `c6ec5bc`  | Accepted            |
| [D-002](#d-002) | 2026-10-12 | Remove template parts that the course does not use                  | Accepted            |
| [D-003](#d-003) | 2026-10-12 | Use labels instead of Issue Types                                   | Accepted            |
| [D-004](#d-004) | 2026-10-12 | Use only synthetic data; real theses default to private             | Accepted            |
| [D-005](#d-005) | 2026-10-12 | Licence prose and data under CC BY 4.0, code under AGPL 3.0         | Accepted            |
| [D-006](#d-006) | 2026-10-12 | Use fictional registration and submission dates                     | Accepted            |
| [D-007](#d-007) | 2026-10-12 | Describe scan reuse, not copyright, in the dataset                  | Accepted            |
| [D-008](#d-008) | 2026-10-12 | Generate pages from YAML instead of executing code                  | Amended by D-012    |
| [D-009](#d-009) | 2026-10-12 | Confirm room F 001; keep pass/fail unresolved                       | Superseded by D-010 |
| [D-010](#d-010) | 2026-10-12 | Use the KSL course entry as the authority; set the pass rule        | Amended by D-014    |
| [D-011](#d-011) | 2026-10-13 | Remove `SPECS.md`; the syllabus and the decisions carry its content | Accepted            |
| [D-012](#d-012) | 2026-10-13 | Link the showcase Project instead of copying it onto the site       | Accepted            |
| [D-013](#d-013) | 2026-10-13 | Give every exercise a browser route and a command-line route        | Accepted            |
| [D-014](#d-014) | 2026-10-27 | Teach X1–X4 as the core; make X5 and X6 optional extensions         | Accepted            |

## D-001 Create the repository from the template at commit `c6ec5bc` {#d-001}

**Context.** The [course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md) (§5) requires that the course repository is created from `maehr/open-research-data-template`. Learners start from the same template.

**Decision.** The repository was created with "Use this template" from commit [`c6ec5bc`](https://github.com/maehr/open-research-data-template/commit/c6ec5bc366c21029e908ad16d54fa0e2201f18ee) of 16 June 2026. `main` starts with the initial commit of the template. All other work, including the course README and the community-health files, arrives through one pull request.

**Consequences.** The course records the template revision. When the template changes, the instructor checks the exercises against the new revision before the next run.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §5 and §6, step 1.

## D-002 Remove template parts that the course does not use {#d-002}

**Context.** The template supports R, Python, Codespaces, a showcase site, and many scaffolds. The course needs a Quarto site and a few Python scripts for the maintainer.

**Decision.** Remove the R stack, the dev container, the showcase site, the template maintenance files, the changelog workflow, and the unused scaffolds. Keep Python through uv for maintainer tooling only.

**Consequences.** CI runs faster and needs no R. Learners do not see these files, because they start from the original template.

**Source.** Maintainer approval of the implementation plan, 12 October 2026.

## D-003 Use labels instead of Issue Types {#d-003}

**Context.** GitHub Issue Types exist only for organisations. A learner works in a personal account.

**Decision.** Mark epics, tasks, and stories with the labels `kind:epic`, `kind:task`, and `kind:story`.

**Consequences.** Every learner can follow the exercises with a free personal account.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §3. GitHub Docs: [Managing issue types in an organization](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization).

## D-004 Use only synthetic data; real theses default to private {#d-004}

**Context.** The exercise repositories are public by default in the workshop. A real thesis can contain personal data, unpublished results, or material with third-party rights.

**Decision.** The public exercise uses only the 30 synthetic records. For real thesis work, the course recommends a private repository and a private Project.

**Consequences.** No real personal or research data enter the public exercise. Exercise X1 includes a visibility check, and the closing block covers the transfer to a private thesis.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §2.

## D-005 Licence prose and data under CC BY 4.0, code under AGPL 3.0 {#d-005}

**Context.** The template releases code under AGPL 3.0 and data under CC BY 4.0. The course adds original teaching prose and screenshots of the GitHub interface.

**Decision.** Original teaching prose and data use CC BY 4.0. Code derived from the template keeps AGPL 3.0. Third-party material keeps its own rights, as [NOTICE.md](../NOTICE.md) lists.

**Consequences.** Others can reuse and adapt the course with attribution. The screenshots are not under CC BY 4.0.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §5 ("Proposed CC BY 4.0"). The instructor confirmed it on 12 October 2026.

## D-006 Use fictional registration and submission dates {#d-006}

**Context.** The real registration and submission dates come from the Dean's Office. They differ per student.

**Decision.** The workshop uses the fictional registration date 2026-12-01 and the fictional submission date 2027-06-01. The six-month gap follows the DH study plan, Art. 15 Abs. 4. Intermediate milestones are adjustable estimates.

**Consequences.** Every page labels these dates as fictional. Real dates stay unconfirmed.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §3. [Studienplan Digital Humanities](https://www.dh.unibe.ch/unibe/portal/fak_historisch/fsuf/d_dh/content/e1644823/e1776786/e1776810/e1777708/Studienplan_DH_Master_Major_Minor_ger.pdf), Art. 15 Abs. 4, p. 5.

## D-007 Describe scan reuse, not copyright, in the dataset {#d-007}

**Context.** A copyright status for fictional 19th-century periodicals would be implausible. The X6 scenario needs a rights restriction.

**Decision.** The column `scan_reuse_status` describes the reuse terms that a fictional archive gives for its scans. Record SYN-P021 is `restricted`.

**Consequences.** The rights restriction in X6 applies to the scans. The CSV itself stays under CC BY 4.0.

**Source.** [Data dictionary](https://github.com/maehr/projm-example-thesis/blob/main/documentation/data-dictionary.qmd) in the example repository.

## D-008 Generate pages from YAML instead of executing code {#d-008}

**Context.** The backlog, the milestones, and the schedule must exist once, as versioned text, and also appear on the website.

**Decision.** `src/render_pages.py` writes Markdown pages from the YAML files. The pages are committed. A test fails when they are stale.

**Consequences.** The site build needs only Quarto. No document executes code.

**Source.** [Course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md), §3 ("Persist the instructor's full example backlog in versioned text").

## D-009 Confirm room F 001; keep pass/fail unresolved {#d-009}

**Context.** The [course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md) (§6, step 4) requires a confirmation of the room, the pass/fail arrangement, the audience mix, and the thesis regulations before release.

**Decision.** The instructor confirmed on 12 October 2026: the room is Seminarraum F 001; the audience is mostly DH Major students; the 2025 DH study plan and RSL Phil.-hist. 21 are the basis of the example; real thesis dates stay unconfirmed. The pass/fail arrangement is not yet confirmed.

**Consequences.** The pages no longer mark the room as unresolved. The pass/fail callout stays. Risks U-01 and U-03 are updated.

**Source.** Instructor confirmation in the implementation session, 12 October 2026.

## D-010 Use the KSL course entry as the authority; set the pass rule {#d-010}

**Context.** Two reviews found the course facts hard to read: the pages cited page numbers of an export, and the pass/fail arrangement stayed open. The KSL course entry lists the exam type as "not defined".

**Decision.** The [KSL course entry](https://www.ksl.unibe.ch/KSL/kurzansicht?stammNr=526141&semester=HS2026&lfdNr=0) is the only source of the course facts. The pages show its fields and link to it. The instructor sets the pass rule: a learner passes when they attend the full session and show the minimum deliverable in the exit check. A labelled recovery package counts.

**Consequences.** The pages drop the export page numbers and the room discrepancy. The pass rule is the instructor's decision, not a KSL rule. Risk U-02 is resolved. [D-014](#d-014) changed the pass rule on 27 October 2026.

**Source.** Instructor decision in the implementation session, 12 October 2026.

## D-011 Remove `SPECS.md`; the syllabus and the decisions carry its content {#d-011}

**Context.** `SPECS.md` was the implementation contract for the first version of the course. After the implementation, each of its rules had a second home: the course facts and outcomes in the syllabus, the conventions in the exercises and the cheat sheet, the build rules in `AGENTS.md`, and the checks in the tests. Two copies of one rule can disagree.

**Decision.** Remove `SPECS.md`. The decisions above cite the specification through a permalink to its last version.

**Consequences.** The syllabus is the entry point for course content. `AGENTS.md` names it as the source of the course facts and the pedagogy.

**Source.** Maintainer request, 13 October 2026. [Last version of the course specification](https://github.com/maehr/github-as-a-project-management-tool/blob/9f180154a3b5e7cb2ea206238502a8d97b2a0711/SPECS.md).

## D-012 Link the showcase Project instead of copying it onto the site {#d-012}

**Context.** The [showcase Project](https://github.com/users/maehr/projects/11) and the [example repository](https://github.com/maehr/projm-example-thesis) hold the full plan of the fictional thesis: 42 Issues, three milestones with their justifications, the pull requests of X4 and X5, the release, and the data dictionary. The site also showed the backlog, the milestones, and the data dictionary as pages. Learners met the same plan twice, and the two copies could disagree.

**Decision.** The site links the showcase Project and the example repository and shows screenshots of them. The copies moved to `archive/`, which Quarto does not render. `project-management/backlog.yml` and `milestones.yml` stay as the source that `src/seed_backlog.py` writes to GitHub. `src/render_pages.py` renders only the schedule and the seven Issue texts that learners copy in X2.

**Consequences.** Decision D-008 now applies to the schedule and the X2 texts only. The seed script creates missing items, but it does not change an existing Issue. A change to an existing Issue therefore goes into `backlog.yml` and into the Issue on GitHub.

**Source.** Maintainer request, 13 October 2026.

## D-013 Give every exercise a browser route and a command-line route {#d-013}

**Context.** The course ran every exercise in the browser only. The KSL entry names minimal command-line knowledge as useful prior knowledge, and a thesis on the learner's own computer needs git. Some learners already use git and gh; others cannot install software on their laptop.

**Decision.** Each exercise step has two routes in tabs: **Browser** and **Command line** (git and gh). Both routes reach the same expected state, so a learner can change the route at any step. A step without a usable command says **Browser only**: the Project field values, the workflows, the Project access, and the status update. The view export has a partial command: gh saves all items of the Project as JSON, but not the filtered view as TSV. The cheat sheet explains version control: why it matters for a thesis, and how a change travels from the working folder to GitHub.

**Consequences.** The Setup page explains how to prepare the command line, and it lists the common command-line problems. The command-line route finds each Issue number by the ID at the start of the title, with the helper `issue`. A command therefore works even when the learner created the Issues in another order. A test checks that every step offers both routes or says "Browser only", and that no Command line tab sends the learner to the browser. The instructor runs the command-line route on the day before the session (risks R-09 and R-10).

**Source.** Maintainer request, 13 October 2026. The command-line route was tested on 13 October 2026 with gh 2.102.0 and git 2.54.0 ([verification log](../course/instructor-notes.qmd#cli-log)).

## D-014 Teach X1–X4 as the core; make X5 and X6 optional extensions {#d-014}

**Context.** The session on 16 October 2026 showed that X1–X6 do not fit into four hours. X5 (35 minutes) and X6 (25 minutes) were the most affected. The exercises cover many GitHub features, but the features do not contribute equally to the learning outcomes. Learners rushed through features instead of understanding the workflow.

**Decision.** Apply the 80/20 principle: classroom time goes to the small set of features that delivers most of the practical value. X1–X4 form the core workshop: repository, Issues, Project, and pull request. X5 and X6 stay complete, but they become optional, self-paced extensions. The run of show gives X1–X4 more time and replaces the X5 and X6 blocks with a block for questions, troubleshooting, and the extensions. Steps in X1–X4 that the core workflow does not need start with **Optional:**. The minimum deliverable and the exit check are removed; an informal closing reflection replaces the exit check. The pass rule of D-010 changes: a learner passes when they attend the full session. No exercise result is required.

**Consequences.** The syllabus, the schedule, the exercise pages, the slides, the instructor notes, and the solutions distinguish core content from optional extensions. A test checks that the schedule holds only X1–X4 and a consolidation block, and that X5 and X6 are marked as optional. The pass rule remains the instructor's decision, not a KSL rule. The session on 16 October 2026 followed version 0.1.0, with the old run of show and the old pass rule.

**Source.** Maintainer request, [issue #17](https://github.com/maehr/github-as-a-project-management-tool/issues/17), 27 October 2026.
