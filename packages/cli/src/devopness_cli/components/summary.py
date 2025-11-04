from dataclasses import dataclass
import json
from typing import Any, Callable, Literal, Optional

import typer
from rich.align import VerticalAlignMethod
from rich.console import Console, JustifyMethod, OverflowMethod, RenderableType
from rich.panel import Panel
from rich.style import StyleType
from rich.table import Table

from devopness_cli.services.devopness_api import devopness

app = typer.Typer()
console = Console()


@dataclass
class SummaryColumn:
    """Configuration for a summary column."""

    # Method to extract the value for this column from a resource
    get_value: Callable[[Any], Any]

    # Column display properties for Rich Table
    header: "RenderableType" = ""
    footer: "RenderableType" = ""
    header_style: Optional[StyleType] = None
    highlight: Optional[bool] = None
    footer_style: Optional[StyleType] = None
    style: Optional[StyleType] = None
    justify: "JustifyMethod" = "left"
    vertical: "VerticalAlignMethod" = "top"
    overflow: "OverflowMethod" = "ellipsis"
    width: Optional[int] = None
    min_width: Optional[int] = None
    max_width: Optional[int] = None
    ratio: Optional[int] = None
    no_wrap: bool = False


def summary(
    data: list[Any],
    resource_name: str,
    columns: list[SummaryColumn],
    page: int,
    page_count: int,
) -> None:
    """
    Print a summary table of a list of resources.
    """

    if not data:
        console.print(f"[bold yellow]No {resource_name.lower()}s found.[/bold yellow]")
        return

    table = Table(
        f"Page {page} of {page_count}",
        show_header=True,
        header_style="bold magenta",
    )

    for column in columns:
        table.add_column(
            header=column.header,
            footer=column.footer,
            header_style=column.header_style,
            highlight=column.highlight,
            footer_style=column.footer_style,
            style=column.style,
            justify=column.justify,
            vertical=column.vertical,
            overflow=column.overflow,
            width=column.width,
            min_width=column.min_width,
            max_width=column.max_width,
            ratio=column.ratio,
            no_wrap=column.no_wrap,
        )

    for resource in data:
        row = [str(column.get_value(resource)) for column in columns]

        table.add_row(*row)

    console.print(table)
