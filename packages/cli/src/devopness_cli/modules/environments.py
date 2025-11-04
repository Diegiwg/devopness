from typing import Literal

import typer
from devopness.models import Environment, EnvironmentRelation
from rich.console import Console

from devopness_cli.components.details import DetailsRow, details
from devopness_cli.components.summary import SummaryColumn, summary
from devopness_cli.components.to_json import to_json
from devopness_cli.services.devopness_api import devopness

app = typer.Typer(
    name="environments",
    help="Manage environments in Devopness.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="list")
def list_environments(
    project_id: int = typer.Option(
        help="ID of the project to list environments for.",
        min=1,
    ),
    page: int = typer.Option(
        help="Page number.",
        default=1,
        min=1,
        show_default=True,
    ),
    per_page: int = typer.Option(
        help="Number of environments per page.",
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
    """List all environments of a project."""
    res = devopness.environments.list_project_environments(project_id, page, per_page)

    environments = res.data

    if format in ("json", "ppjson"):
        return to_json(environments, pretty=format == "ppjson")

    return summary(
        data=environments,
        resource_name="Environment",
        columns=[
            SummaryColumn[EnvironmentRelation](
                header="ID",
                get_value=lambda e: str(e.id),
            ),
            SummaryColumn[EnvironmentRelation](
                header="Name",
                get_value=lambda e: e.name,
            ),
        ],
        page=page,
        page_count=res.page_count,
    )


@app.command(name="get")
def get_environment(
    environment_id: int = typer.Option(
        help="ID of the environment to retrieve.",
        min=1,
    ),
) -> None:
    """Get an environment by ID."""
    res = devopness.environments.get_environment(environment_id)

    environment = res.data

    return details(
        environment,
        [
            DetailsRow[Environment](header="ID", get_value=lambda e: str(e.id)),
            DetailsRow[Environment](header="Name", get_value=lambda e: e.name),
            DetailsRow.line(),
            DetailsRow[Environment](
                header="Created At",
                get_value=lambda e: e.created_at,
            ),
            DetailsRow[Environment](
                header="Updated At",
                get_value=lambda e: e.updated_at,
            ),
        ],
        environment_id,
        "Environment",
    )
