from dataclasses import dataclass
from typing import Any, Callable

from rich.console import Console
from rich.panel import Panel

console = Console()


@dataclass
class DetailsRow:
    """Dataclass to represent a row in a details page."""

    # Method to extract the value for this row from a resource
    get_value: Callable[[Any], Any]

    # Attributes
    header: str
    is_line: bool = False

    @staticmethod
    def line() -> "DetailsRow":
        """Create a line row."""
        return DetailsRow(get_value=lambda x: "", header="", is_line=True)


def details(
    data: Any,  # noqa: ANN401
    rows: list[DetailsRow],
    resource_id: int | str,
    resource_name: str,
) -> None:
    """Render a details page for a resource."""

    if not data:
        empty_state = Panel(
            f"[bold yellow]Could not find {resource_name} "
            f"with ID {resource_id}.[/bold yellow]",
            title=f"{resource_name} Details",
            border_style="yellow",
        )

        console.print(empty_state)
        return

    box = Panel.fit(
        title=f"{resource_name} Details",
        border_style="green",
        renderable="\n".join(
            f"[bold]{row.header}:[/bold] {row.get_value(data)}"
            if not row.is_line
            else ""
            for row in rows
        ),
    )

    console.print(box)
