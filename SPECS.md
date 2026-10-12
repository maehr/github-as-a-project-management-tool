# SPECS.md — GitHub as a Project Management Tool

> **Purpose:** implementation contract for a self-contained, English-language workshop and reusable OER. **Authority:** the [KSL course entry](https://www.ksl.unibe.ch/KSL/kurzansicht?stammNr=526141&semester=HS2026&lfdNr=0) for course facts; instructor brief and prior `SPECS(3).md` for proposed teaching design. Do not present design choices as KSL requirements.

## 1. KSL baseline (authoritative course metadata)

Show the KSL fields on the site and link the KSL entry. Do not cite page numbers of an export.

- **Course:** `[PROJM] Github as a project management tool`; root number **526141**, **HS2026**; type **Workshop**; allocation **Digital Humanities**; lecturer **Dr. Moritz Mähr**, University of Bern, Walter Benjamin Kolleg.
- **Session:** **Friday 16 Oct 2026, 09:00–13:00** (240 minutes); **Seminarraum F 001, Hörraumgebäude Unitobler**.
- **Credits:** **0.5 ECTS**, **passed/failed**; recognition as an optional course possible.
- **Description (KSL):** GitHub can manage and document ongoing projects; the course introduces **different project-management approaches**, combined with best practices for GitHub.
- **Prior knowledge (KSL):** an idea of GitHub and minimal command-line knowledge are ideal; "Introduction to Project Management" is a plus, not a necessity. Design all core exercises for the browser; no software installation or homework prerequisite.
- **Assessment:** KSL lists the exam type as **not defined**. The instructor's pass rule (D-010): attend the full session and show the minimum deliverable in the exit check; a labelled recovery package counts.

## 2. Learning design (instructor proposal, not KSL)

**Narrative:** plan, conduct, document, and responsibly share a **fictional master's thesis** using one GitHub repository and one GitHub Project. Start from [the research-data repository template](https://github.com/new?template_name=open-research-data-template&template_owner=maehr). The **public teaching example** uses 30 labelled **synthetic** periodical-metadata records; **real thesis work defaults to a private repository AND a private Project**. No real personal or research data enter the public exercise.

After 4 hours, each learner should be able to: (1) distinguish repository, Issues, Project, release, and deposit; (2) derive a sourced Issue from an applicable requirement; (3) create epics/sub-issues, one user story, milestones, dependencies, and planning views; (4) complete an Issue through a documentation pull request; (5) decide what can be published; (6) state what GitHub *cannot* guarantee (quality, deadline compliance, confidentiality, long-term preservation).

**Minimum learner deliverable:** repository from template; README adapted to the synthetic thesis; **2 parent epics + 6 native sub-issues** (one user story); **3 milestones**; Project **Backlog, Board, Roadmap**; **1 blocking dependency**; **1 merged documentation PR** with linked Issue; rights/access decision; demo release or explicitly labelled recovery package; decision record. Provide pair/solo and private alternatives.

## 3. GitHub conventions

| Concept | Representation / rule |
| --- | --- |
| Epic | Parent Issue, `kind:epic`; substantial outcome. |
| Task / user story | Native sub-issue, `kind:task` or `kind:story`; output, owner, acceptance criteria, evidence, basis/source. Story wording: “As … I need … so that …”. |
| Dependency | Native `blocked by` relation; **not** a parent-child relation. |
| Milestone | Repository milestone with **justified** due date; formal and proposed dates distinguished. |
| Project | User-owned, linked to repository; separate visibility setting. |
| Views / fields | Backlog (table), Board (status), Roadmap (dates); Status = Backlog/Ready/In progress/In review/Done; Priority = High/Normal/Low; Start/Target date; Basis = Rule/Practice/Demo. |
| Done | Acceptance criteria satisfied, output linked, review and privacy checks done; Issue and Project agree. |

Use browser-accessible GitHub Free features. Labels replace organisation-dependent Issue Types. Do not assume repository templates create Issues, milestones, or Projects; copying a Project does not copy its repository Issues. Persist the instructor's full example backlog in versioned text.

**Example backlog:** E01 Scope/registration; E02 Research design/permissions; E03 Data preparation; E04 Analysis; E05 Writing; E06 Submission; E07 Defence; E08 Publication/preservation. Supply ~4 child tasks per epic in `project-management/backlog.yml`; learners manually build only **E01 and E08** with six sub-issues. Keep scope, dependencies, and evidence consistent. Example story: document CSV columns, types, missing values, synthetic origin, version, and licence for a future reuser.

**Rules vs plans:** The KSL entry governs this **course**, not individual master's theses. For **DH Major** examples, consult the [DH study plan, Arts. 15–16](https://www.dh.unibe.ch/unibe/portal/fak_historisch/fsuf/d_dh/content/e1644823/e1776786/e1776810/e1777708/Studienplan_DH_Master_Major_Minor_ger.pdf) and [faculty rules](https://www.unibe.ch/e152701/e154048/e191232/e205334/e227828/phil_hist_rsl_final_ger.pdf): registration eligibility, confirmed official dates, six-month writing period, length/format, submission, and disputation. Treat rights, ethics, DMP, AI use, archiving, and release as context-dependent tasks, **not universal exam rules**. A DH Minor/elective student must use their actual thesis programme's rules. Each claimed rule needs source, applicability, status, and linked Issue. Keep uncertain real dates unconfirmed. For the workshop only, use **fictional** registration **2026-12-01** and submission **2027-06-01**; intermediate milestones are adjustable estimates.

## 4. Workshop run of show (240 min; 20 min breaks)

| Time | Activity | Learner evidence |
| --- | --- | --- |
| 09:00–09:15 | Frame thesis workflow; compare GitHub objects/PM approaches | Identify tool limits and applicable rules |
| 09:15–09:40 | **X1** Create repository from template | README, synthetic notice, visibility check |
| 09:40–10:15 | **X2** Convert requirements to work | 2 epics, 6 sub-issues, story, criteria |
| 10:15–10:25 | Break | — |
| 10:25–11:05 | **X3** Configure Project | Backlog, Board, Roadmap, 3 milestones, dependency |
| 11:05–11:40 | **X4** Execute one documentation task | Branch → PR → review → merge → Issue closure |
| 11:40–11:50 | Break | — |
| 11:50–12:25 | **X5** Prepare reusable output | Data dictionary, citation/licence check, demo release |
| 12:25–12:50 | **X6** React to delay and restricted source | Update scope/dependency; record decision; export Project view |
| 12:50–13:00 | Private-thesis transfer, exit check | Explain one rule, dependency, and disclosure safeguard |

Provide a short teaching explanation, exact browser steps, annotated screenshots, expected state, and recovery route **for each X1–X6**. No task requires Quarto, Git CLI, paid features, institutional VPN, public disclosure, or a production DOI. Show a fictional two-week source delay and a rights restriction; adjust planned work, **never silently move the official deadline**.

## 5. OER implementation

- **Target:** public `maehr/github-as-a-project-management-tool`, created from [`maehr/open-research-data-template`](https://github.com/maehr/open-research-data-template); site target `https://maehr.github.io/github-as-a-project-management-tool/` (**not assumed deployed**). Students start from the original template, not from a fork of the course site.
- **Toolchain:** Quarto site + Quarto **Reveal.js** slides (`slides/index.qmd`); browser-first handbook. Adapt the [Quarto AGENTS profile and scientific-writing appendix](https://gist.github.com/maehr/6c48ef14f37c9f745fa1fbaa315d106b); keep maintainer tooling out of student prerequisites.
- **Essential paths:** `README.md`, `SPECS.md`, `_quarto.yml`, `index.qmd`, `slides/index.qmd`, `course/{setup,syllabus,exercises/x1-x6,solutions,instructor-notes}.qmd`, `documentation/{requirements,data-dictionary,publication}.qmd`, `project-management/{backlog.yml,milestones.yml,decisions.md,risks.md}`, `data/synthetic-periodicals.csv`, `assets/screenshots/`, `templates/master-thesis/`, `CITATION.cff`, licence notices.
- **Screenshots:** real current GitHub UI captures (not simulated), annotated, dated, privacy-reviewed, with alt text and matching text instructions. Cover template, Issues/sub-issues, Project/visibility, fields/views, dependencies, PR/merge, release, export. Link official documentation next to changing UI procedures. Provide accessible HTML and an offline reading bundle.
- **Reuse:** thesis documentation template covers question, scope, provenance, method, decisions, results, limits, rights, reproducibility, access. Course is an OER **and** a worked documentation example, **not** a university-approved thesis-format template. Proposed CC BY 4.0 for original teaching prose; retain upstream AGPL obligations for derived code and separate third-party rights notices. Never assume public Pages, private Pages, DOI minting, or Zenodo integration is automatic.

## 6. Build order and release gates

1. Inspect upstream template, record revision, adapt metadata/licences; build synthetic scenario and versioned backlog.
2. Test an actual GitHub Free browser journey: create template → add Issues/sub-issues → create Project → dependency/milestones → PR merge/closure → release. Test public **and** private paths.
3. Write X1–X6 plus recovery states; capture annotated screenshots **after** confirming UI behaviour; create Quarto/Reveal.js outputs.
4. Confirm the pass rule, audience mix, and applicable thesis regulations/deadlines. Keep fictional assumptions labelled.
5. Validate exactly **240 minutes**, working links/assets, site + slide rendering, screenshots/alt text, full example backlog, no confidential content or unintended external publishing. Deploy only after explicit approval; verify the live site.

**Source hierarchy:** KSL entry = course facts; university regulations = programme-specific thesis rules; instructor brief/previous SPECS = proposed pedagogy; GitHub/Quarto documentation = changing product behaviour. Cite each at its point of use. **Unresolved information must remain visibly unresolved.**
