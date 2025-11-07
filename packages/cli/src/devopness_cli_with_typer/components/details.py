from dataclasses import dataclass
from typing import Any, Callable, TypeVar

from rich.console import Console, Group
from rich.panel import Panel
from rich.text import Text

console = Console()


T = TypeVar("T")


@dataclass
class DetailsRow[T]:
    """Dataclass to represent a row in a details page."""

    # Method to extract the value for this row from a resource
    get_value: Callable[[T], str]

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
    fullscreen: bool = False,
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

    # Build renderables instead of plain strings
    renderables = []
    for row in rows:
        if row.is_line:
            renderables.append(Text())  # blank line

        else:
            value = row.get_value(data)

            if isinstance(value, (Panel, Group)):
                renderables.append(value)  # type: ignore

            else:
                renderables.append(
                    Text.assemble((f"{row.header}: ", "bold"), str(value))
                )

    group = Group(*renderables)

    box = Panel.fit(
        title=f"{resource_name} Details",
        border_style="green",
        renderable=group,
    )

    box.expand = fullscreen

    console.print(box)
