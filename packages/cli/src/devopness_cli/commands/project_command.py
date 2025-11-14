from cyclopts import App
from rich.console import Console
from rich.table import Table

from devopness_cli.models import BaseOutputModel, BasePageModel, ProjectCreateModel
from devopness_cli.services import devopness

Project = App(
    name="project",
    help="Manage projects in Devopness.",
)

console = Console()


@Project.command(
    name="list",
    help="List all projects.",
)
def list_projects(
    pagination: BasePageModel | None = None,
    output: BaseOutputModel | None = None,
) -> None:
    if pagination is None:
        pagination = BasePageModel()

    if output is None:
        output = BaseOutputModel()

    res = devopness.projects.list_projects(
        page=pagination.page,
        per_page=pagination.per_page,
    )

    if output.format == "table":
        table = Table(title="Projects")

        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")

        for project in res.data:
            table.add_row(
                str(project.id),
                project.name,
            )

        console.print(table)

    elif output.format == "json":
        import json  # noqa: PLC0415

        projects_list = [project.model_dump(mode="json") for project in res.data]

        console.print_json(json.dumps(projects_list, indent=4))

    elif output.format == "plain":
        import json  # noqa: PLC0415

        projects_list = [project.model_dump(mode="json") for project in res.data]

        print(json.dumps(projects_list))


@Project.command(
    name="create",
    help="Create a new project.",
)
def create_project(
    args: ProjectCreateModel,
    output: BaseOutputModel | None = None,
) -> None:
    if output is None:
        output = BaseOutputModel()

    res = devopness.projects.add_project(
        {
            "name": args.name,
        }
    )

    if output.format == "table":
        table = Table(title="Project Created")

        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", style="magenta")

        project = res.data
        table.add_row(
            str(project.id),
            project.name,
        )

        console.print(table)

    elif output.format == "json":
        import json  # noqa: PLC0415

        console.print_json(json.dumps(res.data.model_dump(mode="json"), indent=4))

    elif output.format == "plain":
        import json  # noqa: PLC0415

        print(json.dumps(res.data.model_dump(mode="json")))
