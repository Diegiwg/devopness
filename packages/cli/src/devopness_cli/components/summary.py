from dataclasses import dataclass
from typing import Any, Callable, Optional

from rich.align import VerticalAlignMethod
from rich.console import Console, JustifyMethod, OverflowMethod, RenderableType
from rich.panel import Panel
from rich.style import Style, StyleType
from rich.table import Table

console = Console()


@dataclass
class SummaryColumn:
    """Dataclass to represent a column in a summary table."""

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
        empty_state = Panel(
            f"[bold yellow]No {resource_name.lower()}s found.[/bold yellow]",
            title=f"{resource_name} Summary",
            border_style="yellow",
        )

        console.print(empty_state)
        return

    table = Table(
        caption=f"Page {page} of {page_count}",
        show_header=True,
        header_style=Style(
            bold=True,
        ),
        border_style=Style(
            dim=True,
        ),
        expand=True,
    )

    # First column is always Index
    table.add_column(
        "#",
        style=Style(dim=True),
        justify="right",
        no_wrap=True,
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
            ratio=column.ratio or len(columns),
            no_wrap=column.no_wrap,
        )

    for index, resource in enumerate(data, start=1 + (page - 1) * len(data)):
        row = [str(index)] + [str(column.get_value(resource)) for column in columns]

        table.add_row(*row)

    box = Panel(
        table,
        title=f"{resource_name} Summary",
        border_style="green",
    )

    console.print(box)
