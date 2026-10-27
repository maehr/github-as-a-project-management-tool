# Changelog

All notable changes to this course are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased](https://github.com/maehr/github-as-a-project-management-tool/compare/v0.1.0...HEAD)

### Changed

- X1–X4 form the core workshop; X5 and X6 are optional, self-paced extensions ([#17](https://github.com/maehr/github-as-a-project-management-tool/issues/17), D-014).
- The run of show gives X1–X4 more time and replaces the X5 and X6 blocks with a block for questions, troubleshooting, and the extensions.
- Steps in X1–X4 that the core workflow does not need start with "Optional:".
- The pass rule requires attendance only. An informal closing reflection replaces the minimum deliverable and the exit check.
- The syllabus, the home page, the sidebar, the slides, the solutions, and the instructor notes distinguish core content from optional extensions.

## [0.1.0](https://github.com/maehr/github-as-a-project-management-tool/releases/tag/v0.1.0) - 2026-10-27

The version taught on Friday, 16 October 2026. The tag `v0.1.0` marks commit `280896e`, the state of `main` during the session. The session showed that X1–X6 do not fit into four hours ([#17](https://github.com/maehr/github-as-a-project-management-tool/issues/17)).

### Added

- Course repository created from `maehr/open-research-data-template` at commit `c6ec5bc`.
- Course pages: setup, syllabus, exercises X1–X6, solutions, instructor notes with a UI verification log.
- Reveal.js slides for the session, self-contained for offline use.
- Requirements register with verified rules of the DH study plan (2025) and RSL Phil.-hist. 21.
- Synthetic dataset of 30 periodical records with its data dictionary.
- Versioned example backlog (8 epics, 34 sub-issues), milestones, decisions, and risks.
- Seed script for the example repository and the public showcase Project.
- Annotated screenshots of the GitHub interface, captured on 2026-10-12.
- Thesis documentation template, decision record, and issue forms.
- GitHub cheat sheet with the terms of the workshop, the browser paths, and the matching git and gh commands.
- Page on project-management approaches (phase plan, Kanban, Scrum, and a hybrid), as the KSL description promises.
- Page "After the workshop" with the private-thesis transfer, a weekly review, and a monthly check.
- Three screenshots of the verified Project copy, workflows, and access settings.

### Changed

- Course facts follow the KSL course entry. The pass rule (D-010) and the licence (D-005) are decided.
- Design, fonts, and sidebar navigation follow `maehr/all-data-are-local`. Each exercise opens with "At a glance" and ends with "Next".
- X2: learners derive one Issue from a requirement. X3: learners copy the showcase Project and decide priorities and dates. X6: learners choose and justify one of three options.
- X5 separates coordination, storage, publication, backup, and preservation, and warns that a release archive holds every tracked file.
- The slides cover the whole course, with screenshots.
- The research question matches the synthetic data.
- npm, Python, and GitHub Actions dependencies are updated to their latest releases. Quarto stays at 1.10.19, the latest stable release.

### Fixed

- Project access is separate from repository access in the pair path.
- The example backlog shows the priority of each sub-issue.
- The Project export is a TSV file, and it sits in the view tab menu.
- The extension rule of RSL Art. 56 includes further extensions by the Collegium Decanale.

### Removed

- R stack, dev container, template showcase site, and unused scaffolds of the template.
