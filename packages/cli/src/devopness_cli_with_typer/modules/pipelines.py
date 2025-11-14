import typer
from devopness.models import Pipeline, PipelineRelation
from rich.console import Console

import devopness_cli_with_typer.types as types
from devopness_cli_with_typer.components.details import DetailsRow, details
from devopness_cli_with_typer.components.summary import SummaryColumn, summary
from devopness_cli_with_typer.components.to_json import to_json
from devopness_cli_with_typer.services.devopness_api import devopness

app = typer.Typer(
    name="pipeline",
    help="Manage pipelines in Devopness.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="list")
def list_pipelines(
    resource_id: int = typer.Option(
        help="ID of the resource to list pipelines for.",
        min=1,
    ),
    resource_type: str = typer.Option(
        help="Type of the resource to list pipelines for.",
    ),
    page: types.PageType = types.PageOption,
    per_page: types.PerPageType = types.PerPageOption,
    output: types.OutputType = types.OutputOption,
) -> None:
    res = devopness.pipelines.list_pipelines_by_resource_type(
        resource_id,
        resource_type,
        page,
        per_page,
    )

    pipelines = res.data

    if output in ("json", "text"):
        return to_json(pipelines, pretty=output == "json")

    return summary(
        data=pipelines,
        resource_name="Pipeline",
        columns=[
            SummaryColumn[PipelineRelation](
                header="ID",
                get_value=lambda p: str(p.id),
            ),
            SummaryColumn[PipelineRelation](
                header="Name",
                get_value=lambda p: p.name,
            ),
            SummaryColumn[PipelineRelation](
                header="Operation",
                get_value=lambda p: p.operation,
            ),
        ],
        page=page,
        page_count=res.page_count,
    )


@app.command(name="get")
def get_pipeline(
    pipeline_id: int = typer.Option(
        help="ID of the pipeline to retrieve.",
        min=1,
    ),
) -> None:
    """Get a pipeline by ID."""
    res = devopness.pipelines.get_pipeline(pipeline_id)

    pipeline = res.data

    return details(
        data=pipeline,
        resource_id=pipeline.id,
        resource_name="Pipeline",
        rows=[
            DetailsRow[Pipeline](
                header="ID",
                get_value=lambda p: str(p.id),
            ),
            DetailsRow[Pipeline](
                header="Name",
                get_value=lambda p: p.name,
            ),
            DetailsRow[Pipeline](
                header="Operation",
                get_value=lambda p: p.operation,
            ),
            DetailsRow.line(),
            DetailsRow[Pipeline](
                header="Created At",
                get_value=lambda p: p.created_at,
            ),
            DetailsRow[Pipeline](
                header="Updated At",
                get_value=lambda p: p.updated_at,
            ),
        ],
    )
