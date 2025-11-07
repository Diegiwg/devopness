from cyclopts import App

from devopness_cli.models import BaseOutputModel, BasePageModel, ProjectCreateModel

Project = App(
    name="project",
    help="Manage projects in Devopness.",
)


@Project.command(
    name="list",
    help="List all projects.",
)
def list_projects(
    pagination: BasePageModel | None,
    output: BaseOutputModel | None,
) -> None:
    if pagination is None:
        pagination = BasePageModel()

    if output is None:
        output = BaseOutputModel()

    print(
        f"Listing all projects (page {pagination.page}, per_page {pagination.per_page})..."
    )
    print(f"Output format: {output.format}")


@Project.command(
    name="create",
    help="Create a new project.",
)
def create_project(
    args: ProjectCreateModel,
) -> None:
    print(f"Creating project '{args.name}' with description '{args.description}'...")
