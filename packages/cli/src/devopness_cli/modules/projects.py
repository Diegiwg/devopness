import json
from typing import Literal
import typer
from rich.console import Console
from rich.table import Table

from ..services.devopness_api import devopness

app = typer.Typer()
console = Console()


@app.command(
    name="list",
    help="List all projects.",
)
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
    format: Literal["table", "json"] = typer.Option(  # noqa: A002  # pylint: disable=redefined-builtin
        help="Output format.",
        default="table",
        show_default=True,
    ),
) -> None:
    res = devopness.projects.list_projects(page, per_page)

    if format == "json":
        json_projects = [project.model_dump(mode="json") for project in res.data]

        console.print_json(json.dumps(json_projects))

        return

    table = Table(
        caption=f"Page {page} of {res.page_count}",
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column(
        header="ID",
        style="dim",
        width=6,
    )

    table.add_column(
        header="Name",
        min_width=20,
    )

    table.add_column(
        header="Owner",
    )

    projects = res.data

    for project in projects:
        project_owner = f"@{project.owner.name}"

        table.add_row(
            str(project.id),
            project.name,
            project_owner,
        )

    console.print(table)
