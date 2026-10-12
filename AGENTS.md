# Agents Tooling Specification — Quarto course site

This repository holds the workshop and OER "GitHub as a Project Management Tool" (KSL 526141, HS2026, University of Bern). It is a Quarto website with Reveal.js slides. It derives from [`maehr/open-research-data-template`](https://github.com/maehr/open-research-data-template) at commit `c6ec5bc`.

This file follows the shared [Agents Tooling Specification](https://gist.github.com/maehr/6c48ef14f37c9f745fa1fbaa315d106b): `30-AGENTS.quarto.md`, with the appendices `40-TOOLBELT.macos.md` and `50-WRITING.scientific.md`. Sections 1, 3, 5, and 6 are copied verbatim. Sections 2, 4, and 7 are narrowed to this repository. Section 8 is specific to this repository.

`SPECS.md` is the implementation contract. Read it before you change course content.

**Local deviations from the shared specification:**

* The maintainer owns this repository. Work on a branch and open a pull request. Do not fork.
* The licence files stay as the template ships them: `LICENSE-CCBY.md` for prose and data, `LICENSE-AGPL.md` for code. `NOTICE.md` states the scope.
* `CODE_OF_CONDUCT.md` is Contributor Covenant 2.1 from the template.
* The engine is Python through uv, for maintainer tooling only. No document executes code.

## 1. Orchestration

Context is the scarce resource. Manage it.

**Model tier.** A frontier model holds the plan, the decisions, and the shared context. A small model does a bounded subtask. Pick the tier before you spawn the agent.

**Delegate on evidence.** A subagent starts cold and derives the context again. Delegate work that reads far more than it reports: broad search, log triage, or fan-out over many files. Do a small local edit inline.

**Contracts, not conversations.** Give a subagent one task, the context it cannot infer, the output shape, and the stop condition. A subagent returns a conclusion, never a file dump. Verify a report before you act on it.

**Parallel only when independent.** Run agents at the same time only when no result feeds another. Use three at most.

**Context ladder.** At 25% of the window, name the source of the pressure. At 50%, reduce it: write state to disk, delegate the reading, or narrow the re-reads. At 75%, stop and reduce before further work.

**State on disk.** Write plans, findings, and decisions to files. The transcript dies at the next compaction.

**Read narrow.** Read the slice, not the file. After you write a file, verify the diff or the section you changed. Do not read the whole file again.


## 2. Tooling

`package.json` holds the contract. Call a script. Never call the tool that the script wraps.

| Script | Purpose |
| --- | --- |
| `npm run check` | The gate: Prettier, ruff lint and format check, ty, pytest |
| `npm run format` | Prettier and ruff format |
| `npm run preview` | Quarto preview with live reload |
| `npm run data:generate` | Write `data/synthetic-periodicals.csv` from its seeded generator |
| `npm run pages:render` | Write `project-management/backlog.md`, `milestones.md`, and `course/_schedule.md` from the YAML files |
| `npm run screenshots:annotate` | Draw callouts on raw captures from `assets/screenshots/annotations.yml` |
| `npm run lychee-check` | Check links |
| `npm run changelog:unreleased` | Preview changelog entries |
| `npm run site:build` | Production render. CI only, unless the maintainer asks |
| `npm run release:prepare -- --tag vX.Y.Z` | Site ZIP for a release. Only after maintainer approval |

**Quarto.** [Quarto](https://quarto.org/docs/guide/) 1.10.19, pinned in CI · [quarto-cli-mcp](https://github.com/maehr/quarto-cli-mcp) renders and inspects from an agent session. It builds a temporary project and writes nothing into this repository.

**Engine.** [uv](https://docs.astral.sh/uv/) for Python. Commit `uv.lock`. Python is maintainer tooling: generators, tests, and screenshot annotation. Learners never need it.

**Documents.** [Prettier](https://prettier.io/) formats Markdown, YAML, and JSON · [lychee](https://lychee.cli.rs/) checks links · [prek](https://prek.j178.dev/) runs the hooks · [Commitlint](https://commitlint.js.org/) checks commit messages · [git-cliff](https://git-cliff.org/docs/) writes the changelog.

## 3. Standards

* [SemVer 2.0.0](https://semver.org/) for versions.
* [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.
* [Contributor Covenant 3.0](https://www.contributor-covenant.org/version/3/0/code_of_conduct/) as `CODE_OF_CONDUCT.md`.
* [AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.en.html) as `LICENSE`. SPDX identifier `AGPL-3.0-only`.


## 4. Code

**Preview while you edit.** Preview writes `_site/` and `.quarto/`. That is expected. Commit none of it.

**Run no production render and no publish in an agent session** unless the maintainer asks. That covers `quarto publish`, the deploy workflow, and any release artifact. To check that a document still builds, use `quarto-cli-mcp`. It renders in a temporary project.

* Use `.qmd` for a Quarto page. Use `.md` for text that Quarto renders without change, and for generated pages.
* Give every page valid YAML front matter with a `title`.
* Do not add executed code chunks. Generate a page with a script in `src/` and commit the output. A test fails when the output is stale.
* Cite a source with a link at the point of use. Never invent a source, a rule, or a date.
* Keep `_site/` and `.quarto/` untracked. The project sets no `freeze`.
* Put a new file in the directory that matches its role:

| Path | Role |
| --- | --- |
| `course/` | Setup, syllabus, schedule, exercises X1–X6, solutions, instructor notes |
| `slides/` | Reveal.js slides |
| `documentation/` | Requirements register, data dictionary, publication note |
| `project-management/` | Example backlog and milestones (YAML is the source), decisions, risks |
| `data/` | Synthetic data only |
| `assets/screenshots/` | Annotated screenshots and `annotations.yml` |
| `templates/master-thesis/` | Reusable thesis documentation template and issue forms |
| `src/` | Maintainer scripts |
| `test/` | Tests for course data, backlog consistency, schedule, and assets |

Run the gate before every commit. `prek` runs it too:

```bash
npm run check
```

Add a new tool to that script. The gate runs no preview and no render. A preview never exits, and a production render belongs in CI.

## 5. GitHub Workflow

Use a fork and a pull request. Never push to upstream.

```bash
gh repo fork OWNER/REPO --clone
git switch -c feat/thing
gh pr create --repo OWNER/REPO
```

Allow maintainer edits. Resync with `gh repo sync`. Put one logical change in one PR. Title the PR with a Conventional Commit.

**Stacked PRs.** Each PR targets the branch below it. The bottom PR targets the trunk. Merge from the bottom up. GitHub retargets the rest. Take the requirements from the trunk only. Use the `gh stack` extension. Keep a stack in one repository, never across forks.

**Trunk protection.** Both layers are idempotent, so a second run converges.

```bash
gh repo edit --enable-squash-merge --enable-merge-commit=false --enable-rebase-merge=false \
  --delete-branch-on-merge --allow-update-branch \
  --enable-secret-scanning --enable-secret-scanning-push-protection
gh api -X PUT repos/OWNER/REPO/branches/main/protection --input protection.json
```

The `PUT` replaces the whole configuration. Take the body shape from the [API reference](https://docs.github.com/en/rest/branches/branch-protection), not from a stale snippet.

For a repository with more than one maintainer, enforce a PR before a merge, at least one approval, dismissal of a stale approval on push, code-owner approval, last-push approval, conversation resolution, strict status checks, linear history, `enforce_admins: true`, no force-push, and no deletion. A solo repository differs. See the bullets below.

* Without `enforce_admins`, the rule is advisory for whoever can bypass it.
* A solo repository needs three settings together: 0 required approvals, no required code-owner review, and no required last-push approval. You cannot approve your own pull request, so either of the last two deadlocks the merge even at 0 approvals.
* The free plan covers branch protection on a public repository. Branch protection on a private repository needs Pro.
* Plan limits differ per feature. Secret scanning, push protection, CodeQL, and dependency review are free on a public repository. On a private repository each one needs a paid GitHub security plan. Check the plan before you enable one in a workflow or in `gh repo edit`.
* Rulesets are the successor at organization scale. `gh ruleset` only reads, and creation uses `POST`, so a second run duplicates the ruleset. Prefer the `PUT` for one repository.

## 6. CI/CD Security

Follow [secure use of Actions](https://docs.github.com/en/actions/reference/security/secure-use).

* Set `permissions: contents: read` at the top level. Widen it per job only where a job needs more.
* Default the repository token to read: `gh api -X PUT repos/OWNER/REPO/actions/permissions/workflow -f default_workflow_permissions=read`.
* Pin an action to a full commit SHA. Verify the SHA against the upstream repository, not a fork. Let Dependabot bump it.
* Never check out fork code under `pull_request_target`. Prefer `workflow_run`, and treat its artifacts as untrusted.
* Never interpolate `github.event.*` into `run:`. Pass the value through `env:` and quote `"$VAR"`.
* Use OIDC and a short-lived cloud role. Do not store a long-lived secret. Keep a secret a scalar, never a JSON blob. Rotate it.
* Gate a deploy on an Environment with required reviewers. Prefer an environment secret over a repository secret.
* Do not use a self-hosted runner on a public repository.
* Cover `.github/workflows/**` in `CODEOWNERS`.
* Require the section 4 gate, CodeQL, and `dependency-review-action`. Run the same gate locally, so CI gives no surprise. On a private repository, confirm the plan covers CodeQL and dependency review first.


## 7. Publishing

A GitHub Actions workflow deploys from `main`. Never publish by hand. Never replace the workflow with a manual step.

* Render in CI. The `Render and Publish` workflow builds the site on every pull request. It deploys every push to `main`. A manual run (`gh workflow run quarto-publish.yml --ref <branch>`) deploys the selected branch, if the `github-pages` environment allows that branch.
* The maintainer enables GitHub Pages. Do not enable it, merge to `main`, or create a release without explicit approval.
* Quarto is pinned to 1.10.19 in `quarto-publish.yml` and `release.yml`. Change both together.
* The deploy job alone has `pages: write` and `id-token: write`.
* Keep the site URL in `_quarto.yml`. Do not claim that the site is live before you verify it.
* Never assume that public Pages, private Pages, DOI minting, or Zenodo integration happens automatically.

## 8. Course Content

**Source hierarchy.** Each fact has one source. Cite it at the point of use.

| Fact | Source |
| --- | --- |
| Course facts: date, room, credits, assessment | KSL export of 12 October 2026, as recorded in `SPECS.md` §1 |
| Thesis rules for one programme | That programme's study plan and the faculty regulations |
| Pedagogy and exercise design | `SPECS.md` §2–§4 (instructor proposal, not a KSL requirement) |
| GitHub and Quarto behaviour | Official documentation and the dated UI verification log |

**Rules:**

* Keep an unresolved fact visibly unresolved. Use a callout with the word "Unresolved" and list it in `project-management/risks.md`.
* Never present a design choice as a KSL requirement.
* Label every fictional date as fictional. The workshop uses registration 2026-12-01 and submission 2027-06-01.
* Never move an official deadline silently. Adjust the planned work instead, and record the decision.
* Use only synthetic data in public examples. Real thesis work defaults to a private repository and a private Project.
* Keep the example backlog in `project-management/backlog.yml`. Run `npm run pages:render` after each change.
* Design every core exercise for the browser. No exercise needs Quarto, the Git CLI, paid features, a VPN, public disclosure, or a production DOI.
* Give each exercise a teaching explanation, browser steps, screenshots, the expected state, and a recovery route.
* Capture screenshots from the current GitHub interface after you confirm the behaviour. Give each one a capture date and alt text. Remove avatars, notifications, and unrelated repositories before you commit it.
* Link the official GitHub documentation next to each procedure that depends on the interface.
* Write procedures in Simplified Technical English. Write explanations and arguments by the rules in Appendix B.

## Appendix A. CLI Tooling — macOS

This appendix narrows `40-TOOLBELT.macos.md` to the tools this repository uses. Use Homebrew for system tools.

| Task | Tool |
| --- | --- |
| Text search | `rg` |
| File search | `fd` |
| Markdown lint | `rumdl` |
| YAML front matter and YAML data | `yq` |
| Link check | `lychee` |
| QMD and site production | `quarto` |
| JSON | `jq` |
| CSV | `duckdb` |
| PDF text of a regulation | `pdftotext -layout` |
| Screen capture | `screencapture` (macOS) |

* Read front matter with `yq --front-matter=extract`. Check for `---` on line 1 first.
* Always use `-layout` with `pdftotext`.
* Run `lychee` in CI for the full check. It is slow and reports false errors for sites that return 403.
* If a tool is missing, stop and report it. Do not use a different tool.

## Appendix B. Writing — Scientific Prose

Use these rules for scientific and technical writing in English and German. Apply them to argumentative and expository prose. Do not apply them to code, quoted material, or the bibliography.

### Core rules

1. **Use one term for one concept.** Keep technical terminology stable throughout the text.

2. **Guide the reader actively.** State why a step, distinction, method, or argument is introduced before or while introducing it.

3. **Structure arguments as `Context → Content → Conclusion`.** Give the reader the reason for a point, the point itself, and its implication.

4. **Keep comparisons text-immanent.** When explaining X through Y, make the relevant similarity explicit in the text. Prefer comparisons that can be understood without requiring the reader to recall unrelated examples or external contexts.

5. **Keep logically related statements together.** Develop one line of reasoning at a time.

6. **Express one main idea per sentence and one main function per paragraph.**

7. **Prefer direct verbs and simple grammatical structures.** Use active voice when the actor matters. Prefer verbs over nominalizations and short dependency chains over deeply embedded clauses.

8. **Use parallel form for parallel ideas.** Align the structure of comparisons, alternatives, lists, headings, and argument steps.

9. **Make epistemic status visible.** Distinguish what is observed, inferred, assumed, hypothesized, or uncertain.

10. **Make every sentence earn its place.** Use words and transitions to add factual content, logical structure, qualification, or reader guidance.

### Language profiles

**English:** Use clear international scientific English. Prefer direct, literal wording over idiomatic or ornate phrasing.

**Deutsch:** Verwende klares wissenschaftliches Standarddeutsch. Bevorzuge Verben gegenüber Nominalstil und direkte Satzstrukturen gegenüber Schachtelsätzen.

### Priority

When two rules conflict, follow this order: **Precision → Reader guidance → Explicitness → Consistency → Simplicity → Brevity → Elegance**.

In short:

**One concept, one term.  
Explain why before or while explaining what.  
Keep comparisons local and explicit.  
One sentence, one main idea.  
One paragraph, one line of reasoning.**
