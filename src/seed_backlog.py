"""Seed the example backlog into a GitHub repository and a GitHub Project.

The script reads project-management/backlog.yml and milestones.yml. It creates
labels, milestones, Issues, native sub-issues, "blocked by" dependencies, a
user-owned Project with the course fields and views, and the links from the
Project to one or more repositories. It is idempotent: a second run reuses
what exists.

Dry run by default. Pass --apply to change anything on GitHub.
Requires the GitHub CLI with the scopes `repo` and `project`.

Example:
    uv run python src/seed_backlog.py --repo maehr/projm-example-thesis \\
        --project-title "PROJM example: DH master's thesis" --public \\
        --link-repo maehr/github-as-a-project-management-tool --apply
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from typing import Any

from backlog import Backlog, issue_body, issue_title, load_backlog, load_milestones

RETRIES = 5
TRANSIENT_ERRORS = (
    "temporary conflict",
    "502",
    "503",
    "secondary rate limit",
    "timeout",
)

STATUS_OPTIONS = [
    ("Backlog", "GRAY", "Planned, not ready to start"),
    ("Ready", "BLUE", "Ready to start: inputs and acceptance criteria are clear"),
    ("In progress", "YELLOW", "Work has started"),
    ("In review", "PURPLE", "Waiting for review by a peer or the supervisor"),
    ("Done", "GREEN", "Acceptance criteria met, output linked, checks done"),
]
PRIORITY_OPTIONS = [
    ("High", "RED", ""),
    ("Normal", "YELLOW", ""),
    ("Low", "GRAY", ""),
]
BASIS_OPTIONS = [
    ("Rule", "ORANGE", "A regulation requires it. Cite the source."),
    ("Practice", "BLUE", "Good practice. Depends on the context."),
    ("Demo", "PINK", "Exists only for the workshop."),
]
VIEWS = [
    # (name, layout, filter)
    ("Backlog", "TABLE_LAYOUT", ""),
    ("Board", "BOARD_LAYOUT", "-label:kind:epic"),
    ("Roadmap", "ROADMAP_LAYOUT", ""),
]

PROJECT_DESCRIPTION = (
    "Worked example: a fictional DH master's thesis planned with GitHub Issues, "
    "sub-issues, milestones, and dependencies. Synthetic data only."
)
PROJECT_README = """\
# PROJM example: DH master's thesis

This Project belongs to the workshop **GitHub as a Project Management Tool**
(University of Bern, HS2026):
<https://github.com/maehr/github-as-a-project-management-tool>

> The thesis, the people, and the dates are fictional. The data are synthetic.
> The two dates 2026-12-01 (registration) and 2027-06-01 (submission) stand in
> for official dates. Never move an official date silently.

## What you see

- **Epics** E01 to E08 are parent Issues with the label `kind:epic`.
- **Tasks and stories** are native sub-issues (`kind:task`, `kind:story`).
- **Dependencies** use the native "blocked by" relation, not the hierarchy.
- **Milestones** M1 to M3 are repository milestones with justified dates.

## Fields

| Field | Values |
| --- | --- |
| Status | Backlog, Ready, In progress, In review, Done |
| Priority | High, Normal, Low |
| Start date, Target date | Planned dates |
| Basis | Rule (a regulation requires it), Practice, Demo |

## Views

- **Backlog**: table of all Issues.
- **Board**: tasks and stories by Status.
- **Roadmap**: tasks and stories on a timeline by Start date and Target date.

## Reuse

Open the menu (…) of this Project and select **Make a copy**. The copy keeps
the fields and the views. It does not copy the Issues. For a real thesis, keep
the repository and the Project **private**.

The versioned source of this backlog is
`project-management/backlog.yml` in the course repository.
"""


class GitHub:
    """Thin wrapper around the gh CLI with a dry-run mode."""

    def __init__(self, apply: bool) -> None:
        self.apply = apply

    def read(self, *args: str) -> str:
        result = subprocess.run(
            ["gh", *args], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            raise RuntimeError(f"gh {' '.join(args)} failed:\n{result.stderr}")
        return result.stdout

    def read_json(self, *args: str) -> Any:
        return json.loads(self.read(*args) or "null")

    def write(self, description: str, *args: str, payload: Any = None) -> Any:
        if not self.apply:
            print(f"[dry run] {description}")
            return None
        command = ["gh", *args]
        stdin = None
        if payload is not None:
            command += ["--input", "-"]
            stdin = json.dumps(payload)
        for attempt in range(1, RETRIES + 1):
            result = subprocess.run(
                command, input=stdin, capture_output=True, text=True, check=False
            )
            transient = any(word in result.stderr for word in TRANSIENT_ERRORS)
            if result.returncode == 0 or not transient or attempt == RETRIES:
                break
            time.sleep(2 * attempt)
        if result.returncode != 0:
            raise RuntimeError(f"{description} failed:\n{result.stderr}")
        print(f"[applied] {description}")
        return json.loads(result.stdout) if result.stdout.strip() else None

    def query(self, query: str, **variables: Any) -> Any:
        """Run a read-only GraphQL query, also in a dry run."""
        payload = json.dumps({"query": query, "variables": variables})
        result = subprocess.run(
            ["gh", "api", "graphql", "--input", "-"],
            input=payload,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)["data"]

    def graphql(self, description: str, query: str, **variables: Any) -> Any:
        payload = {"query": query, "variables": variables}
        return self.write(description, "api", "graphql", payload=payload)


def paginate(gh: GitHub, path: str) -> list[dict[str, Any]]:
    pages = gh.read("api", "--paginate", "--slurp", path)
    return [entry for page in json.loads(pages) for entry in page]


def seed_repository(
    gh: GitHub, repo: str, backlog: Backlog, items: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Create labels, milestones, Issues, sub-issues, and dependencies."""
    for label in backlog.labels:
        gh.write(
            f"label {label['name']}",
            "label",
            "create",
            label["name"],
            "--repo",
            repo,
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
        )

    existing_milestones = {
        m["title"]: m for m in paginate(gh, f"repos/{repo}/milestones?state=all")
    }
    milestone_numbers: dict[str, int] = {}
    for milestone in load_milestones():
        title = f"{milestone['id']} {milestone['title']}"
        if title in existing_milestones:
            milestone_numbers[milestone["id"]] = existing_milestones[title]["number"]
            continue
        description = f"{milestone['date_status']}: {' '.join(milestone['justification'].split())}"
        created = gh.write(
            f"milestone {title}",
            "api",
            f"repos/{repo}/milestones",
            payload={
                "title": title,
                "due_on": f"{milestone['due']}T12:00:00Z",
                "description": description,
            },
        )
        milestone_numbers[milestone["id"]] = created["number"] if created else 0

    existing_issues = {
        issue["title"]: issue
        for issue in paginate(gh, f"repos/{repo}/issues?state=all&per_page=100")
        if "pull_request" not in issue
    }
    issues: dict[str, dict[str, Any]] = {}
    for item in items:
        title = issue_title(item)
        if title in existing_issues:
            issues[item["id"]] = existing_issues[title]
            continue
        payload: dict[str, Any] = {
            "title": title,
            "body": issue_body(item, backlog),
            "labels": [f"kind:{item['kind']}"],
        }
        if item.get("milestone"):
            payload["milestone"] = milestone_numbers[item["milestone"]]
        created = gh.write(
            f"issue {title}", "api", f"repos/{repo}/issues", payload=payload
        )
        issues[item["id"]] = created or {"id": 0, "number": 0, "html_url": ""}

    item_ids = {item["id"] for item in items}
    for item in items:
        if item["kind"] == "epic":
            continue
        parent = issues[item["parent"]]
        child = issues[item["id"]]
        if gh.apply:
            current = {
                s["id"]
                for s in paginate(
                    gh, f"repos/{repo}/issues/{parent['number']}/sub_issues"
                )
            }
            if child["id"] in current:
                continue
        gh.write(
            f"sub-issue {item['id']} under {item['parent']}",
            "api",
            f"repos/{repo}/issues/{parent['number']}/sub_issues",
            payload={"sub_issue_id": child["id"]},
        )

    for item in items:
        for blocker_id in item.get("blocked_by", []):
            if blocker_id not in item_ids:
                continue
            issue = issues[item["id"]]
            blocker = issues[blocker_id]
            if gh.apply:
                current = {
                    b["id"]
                    for b in paginate(
                        gh,
                        f"repos/{repo}/issues/{issue['number']}/dependencies/blocked_by",
                    )
                }
                if blocker["id"] in current:
                    continue
            gh.write(
                f"dependency {item['id']} blocked by {blocker_id}",
                "api",
                f"repos/{repo}/issues/{issue['number']}/dependencies/blocked_by",
                payload={"issue_id": blocker["id"]},
            )
    return issues


def find_project(gh: GitHub, owner: str, title: str) -> dict[str, Any] | None:
    projects = gh.read_json(
        "project", "list", "--owner", owner, "--format", "json", "--limit", "100"
    )
    for project in projects["projects"]:
        if project["title"] == title:
            return project
    return None


def options_payload(
    options: list[tuple[str, str, str]], existing: dict[str, str]
) -> list[dict[str, str]]:
    payload = []
    for name, color, description in options:
        option = {"name": name, "color": color, "description": description}
        if name in existing:
            option["id"] = existing[name]
        payload.append(option)
    return payload


UPDATE_FIELD = """
mutation($fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]) {
  updateProjectV2Field(input: {fieldId: $fieldId, singleSelectOptions: $options}) {
    projectV2Field { ... on ProjectV2SingleSelectField { id } }
  }
}"""
CREATE_FIELD = """
mutation($projectId: ID!, $name: String!, $dataType: ProjectV2CustomFieldType!,
         $options: [ProjectV2SingleSelectFieldOptionInput!]) {
  createProjectV2Field(input: {projectId: $projectId, name: $name,
                               dataType: $dataType, singleSelectOptions: $options}) {
    projectV2Field { ... on ProjectV2FieldCommon { id } }
  }
}"""
PROJECT_FIELDS = """
query($projectId: ID!) {
  node(id: $projectId) {
    ... on ProjectV2 {
      fields(first: 50) {
        nodes {
          ... on ProjectV2FieldCommon { id name dataType }
          ... on ProjectV2SingleSelectField { options { id name } }
        }
      }
      views(first: 20) { nodes { id name layout } }
    }
  }
}"""
CREATE_VIEW = """
mutation($projectId: ID!, $name: String!, $layout: ProjectV2ViewLayout!,
         $fieldIds: [ID!]) {
  createProjectV2View(input: {projectId: $projectId, name: $name, layout: $layout,
                              configuration: {visibleFieldIds: $fieldIds}}) {
    projectV2View { id }
  }
}"""
UPDATE_VIEW = """
mutation($viewId: ID!, $name: String, $filter: String, $fieldIds: [ID!]) {
  updateProjectV2View(input: {viewId: $viewId, name: $name, filter: $filter,
                              configuration: {visibleFieldIds: $fieldIds}}) {
    projectV2View { id }
  }
}"""
CREATE_VIEW_PLAIN = """
mutation($projectId: ID!, $name: String!, $layout: ProjectV2ViewLayout!) {
  createProjectV2View(input: {projectId: $projectId, name: $name, layout: $layout}) {
    projectV2View { id }
  }
}"""
UPDATE_VIEW_PLAIN = """
mutation($viewId: ID!, $name: String, $filter: String) {
  updateProjectV2View(input: {viewId: $viewId, name: $name, filter: $filter}) {
    projectV2View { id }
  }
}"""
SET_VALUE = """
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: ProjectV2FieldValue!) {
  updateProjectV2ItemFieldValue(input: {projectId: $projectId, itemId: $itemId,
                                        fieldId: $fieldId, value: $value}) {
    projectV2Item { id }
  }
}"""


def project_state(gh: GitHub, project_id: str) -> dict[str, Any]:
    node = gh.query(PROJECT_FIELDS, projectId=project_id)["node"]
    fields = {f["name"]: f for f in node["fields"]["nodes"] if f}
    views = {v["name"]: v for v in node["views"]["nodes"]}
    return {"fields": fields, "views": views}


def seed_project(
    gh: GitHub,
    owner: str,
    title: str,
    public: bool,
    link_repos: list[str],
    backlog: Backlog,
    items: list[dict[str, Any]],
    issues: dict[str, dict[str, Any]],
) -> None:
    project = find_project(gh, owner, title)
    if project is None:
        project = gh.write(
            f"project {title}",
            "project",
            "create",
            "--owner",
            owner,
            "--title",
            title,
            "--format",
            "json",
        )
    if project is None:
        print("[dry run] stop: the remaining Project steps need the Project id")
        return
    number = str(project["number"])
    project_id = project["id"]
    gh.write(
        f"project {number}: visibility, description, README",
        "project",
        "edit",
        number,
        "--owner",
        owner,
        "--visibility",
        "PUBLIC" if public else "PRIVATE",
        "--description",
        PROJECT_DESCRIPTION,
        "--readme",
        PROJECT_README,
    )
    for repo in link_repos:
        try:
            gh.write(
                f"link project {number} to {repo}",
                "project",
                "link",
                number,
                "--owner",
                owner,
                "--repo",
                repo,
            )
        except RuntimeError as error:
            print(f"[skipped] link to {repo}: {str(error).splitlines()[-1]}")

    state = project_state(gh, project_id)
    fields = state["fields"]
    status = fields["Status"]
    gh.graphql(
        "Status options",
        UPDATE_FIELD,
        fieldId=status["id"],
        options=options_payload(
            STATUS_OPTIONS, {o["name"]: o["id"] for o in status["options"]}
        ),
    )
    custom = [
        ("Priority", "SINGLE_SELECT", PRIORITY_OPTIONS),
        ("Start date", "DATE", None),
        ("Target date", "DATE", None),
        ("Basis", "SINGLE_SELECT", BASIS_OPTIONS),
    ]
    for name, data_type, options in custom:
        if name in fields:
            continue
        variables: dict[str, Any] = {
            "projectId": project_id,
            "name": name,
            "dataType": data_type,
        }
        if options:
            variables["options"] = options_payload(options, {})
        gh.graphql(f"field {name}", CREATE_FIELD, **variables)

    state = project_state(gh, project_id)
    fields = state["fields"]
    visible = [
        fields[name]["id"]
        for name in (
            "Title",
            "Status",
            "Priority",
            "Basis",
            "Milestone",
            "Start date",
            "Target date",
            "Labels",
            "Parent issue",
        )
        if name in fields
    ]
    views = state["views"]
    for index, (name, layout, filter_text) in enumerate(VIEWS):
        if name in views:
            view_id = views[name]["id"]
        elif index == 0 and len(views) == 1:
            # Rename the default view that every new Project has.
            view_id = next(iter(views.values()))["id"]
        else:
            # Roadmap views do not support a list of visible fields.
            fields_kw = {} if layout == "ROADMAP_LAYOUT" else {"fieldIds": visible}
            created = gh.graphql(
                f"view {name}",
                CREATE_VIEW_PLAIN if layout == "ROADMAP_LAYOUT" else CREATE_VIEW,
                projectId=project_id,
                name=name,
                layout=layout,
                **fields_kw,
            )
            view_id = created["data"]["createProjectV2View"]["projectV2View"]["id"]
        roadmap = layout == "ROADMAP_LAYOUT"
        gh.graphql(
            f"view {name}: name, filter, fields",
            UPDATE_VIEW_PLAIN if roadmap else UPDATE_VIEW,
            viewId=view_id,
            name=name,
            filter=filter_text,
            **({} if roadmap else {"fieldIds": visible}),
        )

    existing_items = gh.read_json(
        "project",
        "item-list",
        number,
        "--owner",
        owner,
        "--format",
        "json",
        "--limit",
        "500",
    )
    item_by_url = {
        entry["content"].get("url"): entry["id"]
        for entry in existing_items["items"]
        if entry.get("content")
    }

    def option_id(field: str, name: str) -> str:
        return next(o["id"] for o in fields[field]["options"] if o["name"] == name)

    for item in items:
        url = issues[item["id"]]["html_url"]
        item_id = item_by_url.get(url)
        if item_id is None:
            added = gh.write(
                f"add {item['id']} to project",
                "project",
                "item-add",
                number,
                "--owner",
                owner,
                "--url",
                url,
                "--format",
                "json",
            )
            item_id = added["id"]
        if item["kind"] == "epic":
            start, target = backlog.epic_dates(item["id"])
            values: dict[str, Any] = {}
        else:
            start, target = item["start"], item["target"]
            values = {
                "Priority": {
                    "singleSelectOptionId": option_id("Priority", item["priority"])
                },
                "Basis": {"singleSelectOptionId": option_id("Basis", item["basis"])},
            }
        values["Status"] = {"singleSelectOptionId": option_id("Status", "Backlog")}
        values["Start date"] = {"date": str(start)}
        values["Target date"] = {"date": str(target)}
        for field_name, value in values.items():
            gh.graphql(
                f"{item['id']}: {field_name}",
                SET_VALUE,
                projectId=project_id,
                itemId=item_id,
                fieldId=fields[field_name]["id"],
                value=value,
            )
    print(f"Project: {project.get('url', number)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument("--repo", required=True, help="OWNER/REPO for the Issues")
    parser.add_argument("--project-title", required=True)
    parser.add_argument("--public", action="store_true", help="Make the Project public")
    parser.add_argument(
        "--link-repo",
        action="append",
        default=[],
        help="Extra OWNER/REPO to link the Project to (repeatable)",
    )
    parser.add_argument(
        "--learner-only",
        action="store_true",
        help="Seed only E01 and E08 with the six learner sub-issues",
    )
    parser.add_argument("--apply", action="store_true", help="Change GitHub")
    args = parser.parse_args()

    backlog = load_backlog()
    items = [
        item for item in backlog.items if not args.learner_only or item.get("learner")
    ]
    gh = GitHub(apply=args.apply)
    if not args.apply:
        print("Dry run. Pass --apply to change GitHub.", file=sys.stderr)
    issues = seed_repository(gh, args.repo, backlog, items)
    owner = args.repo.split("/")[0]
    seed_project(
        gh,
        owner,
        args.project_title,
        args.public,
        [args.repo, *args.link_repo],
        backlog,
        items,
        issues,
    )


if __name__ == "__main__":
    main()
