import json
from typing import Any

from rich.console import Console

console = Console()


def to_json(data: Any, pretty: bool = False) -> None:  # noqa: ANN401
    """Print data as JSON."""
    if not data:
        console.print("")
        return

    if isinstance(data, list):
        data = [el.model_dump(mode="json") for el in data]

    if hasattr(data, "model_dump"):
        data = data.model_dump(mode="json")

    json_data = json.dumps(data)

    if pretty:
        console.print_json(json_data)
    else:
        print(json_data)
