from typing import Literal

import typer

ResourceIdType = int
ResourceIdOption: ResourceIdType = typer.Option(
    help="ID of the argument resource.",
    min=1,
)

OutputType = Literal["table", "json", "text"]
OutputOption: OutputType = typer.Option(
    help="Output format.",
    default="table",
    show_default=True,
)

PageType = int
PageOption: PageType = typer.Option(
    help="Page number.",
    default=1,
    min=1,
    show_default=True,
)

PerPageType = int
PerPageOption: PerPageType = typer.Option(
    help="Number of environments per page.",
    default=20,
    min=1,
    max=100,
    show_default=True,
)
