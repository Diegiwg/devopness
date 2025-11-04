from typing import Literal

import typer
from rich.console import Console
from rich.panel import Panel

from devopness_cli.components.summary import SummaryColumn, summary
from devopness_cli.components.to_json import to_json
from devopness_cli.services.devopness_api import devopness
from devopness_cli.components.details import details, DetailsRow

app = typer.Typer()
console = Console()


@app.command(name="list")
def list_projects(
    page: int = typer.Option(
        help="Page number.",
        default=1,
        min=1,
        show_default=True,
    ),
    per_page: int = typer.Option(
        help="Number of projects per page.",
        default=20,
        min=1,
        max=100,
        show_default=True,
    ),
    format: Literal["table", "ppjson", "json"] = typer.Option(  # noqa: A002  # pylint: disable=redefined-builtin
        help="Output format.",
        default="table",
        show_default=True,
    ),
) -> None:
    """List all projects."""
    res = devopness.projects.list_projects(page, per_page)

    if format in ("json", "ppjson"):
        return to_json(res.data, pretty=format == "ppjson")

    return summary(
        data=res.data,
        resource_name="Project",
        columns=[
            SummaryColumn(header="ID", get_value=lambda p: str(p.id)),
            SummaryColumn(header="Name", get_value=lambda p: p.name),
            SummaryColumn(header="Owner", get_value=lambda p: f"@{p.owner.name}"),
        ],
        page=page,
        page_count=res.page_count,
    )


@app.command(name="get")
def get_project(
    project_id: int = typer.Option(
        help="ID of the project to retrieve.",
        min=1,
    ),
) -> None:
    """Get a project by ID."""
    res = devopness.projects.get_project(project_id)

    project = res.data

    return details(
        project,
        [
            DetailsRow(header="ID", get_value=lambda p: p.id),
            DetailsRow(header="Name", get_value=lambda p: p.name),
            DetailsRow(header="Owner", get_value=lambda p: f"@{p.owner.name}"),
            DetailsRow.line(),
            DetailsRow(header="Created At", get_value=lambda p: p.created_at),
            DetailsRow(header="Updated At", get_value=lambda p: p.updated_at),
        ],
        project_id,
        "Project",
    )
