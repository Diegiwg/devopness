from typing import cast

import typer
from devopness.models import Application, ApplicationRelation, CredentialRelation
from rich.console import Console

import devopness_cli_with_typer.types as types
from devopness_cli_with_typer.components.details import DetailsRow, details
from devopness_cli_with_typer.components.summary import SummaryColumn, summary
from devopness_cli_with_typer.components.to_json import to_json
from devopness_cli_with_typer.services.devopness_api import devopness

app = typer.Typer(
    name="application",
    help="Manage applications in Devopness.",
    no_args_is_help=True,
)

console = Console()


def get_application_repository_url(
    application: Application | ApplicationRelation,
) -> str:
    """Get the repository URL for a given application."""
    credential = cast(CredentialRelation, application.credential)

    url = f"https://{credential.provider.code}.com/{application.repository}"

    return f"[link={url}]{application.repository}[/link]"


def get_application_stack(application: Application | ApplicationRelation) -> str:
    """Get the stack string for a given application."""

    stack = application.programming_language

    has_engine_version = application.engine_version.lower() != "none"

    if has_engine_version:
        stack += f" {application.engine_version}"

    has_framework = application.framework.lower() != "none"

    if has_framework:
        stack += f" ({application.framework})"

    return stack


@app.command(name="list")
def list_applications(
    environment_id: int = typer.Option(
        help="ID of the environment to list applications for.",
        min=1,
    ),
    page: types.PageType = types.PageOption,
    per_page: types.PerPageType = types.PerPageOption,
    output: types.OutputType = types.OutputOption,
) -> None:
    """List all applications of a environment."""
    res = devopness.applications.list_environment_applications(
        environment_id,
        page,
        per_page,
    )

    applications = res.data

    if output in ("json", "text"):
        return to_json(applications, pretty=output == "json")

    return summary(
        data=applications,
        resource_name="Application",
        columns=[
            SummaryColumn[ApplicationRelation](
                header="ID",
                get_value=lambda a: str(a.id),
            ),
            SummaryColumn[ApplicationRelation](
                header="Name",
                get_value=lambda a: a.name,
            ),
            SummaryColumn[ApplicationRelation](
                header="Repository",
                get_value=get_application_repository_url,
            ),
            SummaryColumn[ApplicationRelation](
                header="Stack (Language, Version, Framework)",
                get_value=get_application_stack,
            ),
        ],
        page=page,
        page_count=res.page_count,
    )


@app.command(name="get")
def get_application(
    application_id: int = typer.Option(
        help="ID of the application to retrieve.",
        min=1,
    ),
) -> None:
    """Get an application by ID."""
    res = devopness.applications.get_application(application_id)

    application = res.data

    return details(
        application,
        [
            DetailsRow[Application](
                header="ID",
                get_value=lambda a: str(a.id),
            ),
            DetailsRow[Application](
                header="Name",
                get_value=lambda a: a.name,
            ),
            DetailsRow.line(),
            DetailsRow[Application](
                header="Created At",
                get_value=lambda a: a.created_at,
            ),
            DetailsRow[Application](
                header="Updated At",
                get_value=lambda a: a.updated_at,
            ),
        ],
        application_id,
        "Application",
    )
