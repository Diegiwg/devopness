import json
import re
import shlex
from os import abort
from typing import Any, List, Union, cast

import click
import typer
from devopness.models import (
    Hook,
    HookIncomingSettings,
    HookIncomingSettingsPlain,
    HookPipelineCreate,
    HookPipelineCreatePlain,
    HookPipelineCreateSettings,
    HookPipelineCreateSettingsPlain,
    HookRelation,
    HookTriggerWhen,
    HookTypeParam,
    HookTypeParamPlain,
    HookVariable,
    HookVariableType,
    TriggerWhenConditionType,
)
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text

import devopness_cli_with_typer.types as types
from devopness_cli_with_typer.components.details import DetailsRow, details
from devopness_cli_with_typer.components.summary import SummaryColumn, summary
from devopness_cli_with_typer.components.to_json import to_json
from devopness_cli_with_typer.services.devopness_api import devopness

app = typer.Typer(
    name="hook",
    help="Manage hooks in Devopness.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="list")
def list_hooks(
    pipeline_id: int = typer.Option(
        help="ID of the pipeline to list hooks for.",
        min=1,
    ),
    page: types.PageType = types.PageOption,
    per_page: types.PerPageType = types.PerPageOption,
    output: types.OutputType = types.OutputOption,
) -> None:
    """List all hooks of a pipeline."""
    res = devopness.hooks.list_pipeline_hooks(
        pipeline_id,
        page,
        per_page,
    )

    hooks = res.data

    if output in ("json", "text"):
        return to_json(hooks, pretty=output == "json")

    return summary(
        data=hooks,
        resource_name="Hook",
        columns=[
            SummaryColumn[HookRelation](
                header="ID",
                get_value=lambda p: str(p.id),
            ),
            SummaryColumn[HookRelation](
                header="Name",
                get_value=lambda p: p.name,
            ),
        ],
        page=page,
        page_count=res.page_count,
    )


# @app.command(name="get")


create_app = typer.Typer(
    name="create",
    help="Create a hook for a pipeline.",
    no_args_is_help=True,
)

app.add_typer(create_app)


def parse_hook_variable(value: str) -> HookVariable:
    """
    Parse a CLI argument like:
      name="application id",type=integer,required=true,default_value=123
    and convert it into a HookVariable instance.
    """
    try:
        # Split safely, respecting quotes
        parts = [p.strip() for p in shlex.split(value.replace(",", " ")) if "=" in p]

        parsed = {}
        for part in parts:
            key, raw_value = part.split("=", 1)

            key = key.strip()
            raw_value = raw_value.strip().strip('"').strip("'")

            if key not in (
                "name",
                "path",
                "type",
                "required",
                "default_value",
            ):
                raise ValueError(f"Unknown key '{key}' in hook variable.")

            # type conversion
            if raw_value.lower() in {"true", "false"}:
                parsed[key] = raw_value.lower() == "true"

            elif raw_value.isdigit():
                parsed[key] = int(raw_value)  # type: ignore[assignment]

            elif raw_value.startswith(("[", "{")):
                try:
                    parsed[key] = json.loads(raw_value)
                except json.JSONDecodeError:
                    parsed[key] = raw_value  # type: ignore[assignment]

            else:
                parsed[key] = raw_value  # type: ignore[assignment]

        variable = {}

        if "name" in parsed:
            variable["name"] = parsed["name"]

        if "path" in parsed:
            variable["path"] = parsed["path"]

        if "type" in parsed:
            variable["type"] = parsed["type"]

        if "required" in parsed:
            variable["required"] = parsed["required"]

        if "default_value" in parsed:
            variable["default_value"] = parsed["default_value"]

        return HookVariable.from_dict(variable)

    except Exception as e:
        raise typer.BadParameter(
            f"Invalid --hook-variable format: {value}\nError: {e}",
        ) from e


def parse_hook_trigger_when(value: str) -> HookTriggerWhen:
    """
    Parse a CLI argument like:
      kind=event,name="payload.received"
      kind=condition,name=owner,path="data.owner.username",accepted_values=["admin","dev"]
    and convert it into a HookTriggerWhen instance.
    """
    try:
        # Split safely, respecting quotes
        parts = [p.strip() for p in shlex.split(value.replace(",", " ")) if "=" in p]

        parsed = {}
        for part in parts:
            key, raw_value = part.split("=", 1)

            key = key.strip()
            value = raw_value.strip().strip('"').strip("'")

            if key not in (
                "kind",
                "name",
                "path",
                "accepted_values",
            ):
                raise ValueError(f"Unknown key '{key}' in hook trigger when.")

            if key == "kind" and value not in {"event", "condition"}:
                raise ValueError(
                    f"Invalid value '{value}' "
                    "for key 'kind'. Must be 'event' or 'condition'."
                )

            # type conversion
            if value.startswith(("[", "{")):
                try:
                    fixed = re.sub(r"(?<=\[)([A-Za-z0-9_\-]+)(?=[,\]])", r'"\1"', value)
                    parsed[key] = json.loads(fixed)

                except json.JSONDecodeError:
                    parsed[key] = value  # type: ignore[assignment]

            else:
                parsed[key] = value  # type: ignore[assignment]

        data: dict[str, Any] = {
            "events": [],
            "conditions": [],
        }

        if parsed["kind"] == "event":
            if "name" not in parsed:
                raise ValueError("Missing 'name' for event trigger.")

            data["events"].append(parsed["name"])

        if parsed["kind"] == "condition":
            if "path" not in parsed:
                raise ValueError("Missing 'path' for condition trigger.")

            if "accepted_values" not in parsed:
                raise ValueError("Missing 'accepted_values' for condition trigger.")

            condition: dict[str, Any] = {
                "path": parsed["path"],
                "type": TriggerWhenConditionType.REQUEST_BODY,
                "accepted_values": parsed["accepted_values"],
            }

            if "name" in parsed:
                condition["name"] = parsed["name"]

            data["conditions"].append(condition)

        return HookTriggerWhen.from_dict(data)

    except Exception as e:
        raise typer.BadParameter(
            f"Invalid --hook-trigger-when format: {value}\nError: {e}",
        ) from e


@create_app.command(name="incoming")
def create_incoming_hook(
    pipeline_id: int = typer.Option(
        help="ID of the pipeline to create a hook for.",
        min=1,
    ),
    hook_name: str = typer.Option(
        help="Name of the hook to create.",
    ),
    hook_requires_secret: bool = typer.Option(
        False,
        help="Whether the hook requires a secret token.",
    ),
    hook_trigger_when: List[HookTriggerWhen] = typer.Option(  # noqa: B008
        [],
        "--hook-trigger-when",
        parser=parse_hook_trigger_when,
        help="Define conditions to trigger the hook. Can be used multiple times.\n\n\n\n"  # noqa: E501
        "Keys:\n\n",
    ),
    hook_variables: List[HookVariable] = typer.Option(  # noqa: B008
        [],
        "--hook-variable",
        parser=parse_hook_variable,
        help="Define variables to include in the hook payload."
        " Can be used multiple times.\n\n\n\n"
        "Keys:\n\n"
        "* name (str): Name of the variable\n\n"
        "* path (str): JSON path to extract the variable from the payload (if not defined the name will be used).\n\n"  # noqa: E501
        "* type (str): Type of the variable. One of: string, integer, boolean, array, object.\n\n"  # noqa: E501
        "* required (bool): Whether the variable is required.\n\n"
        "* default_value (str): Default value for the variable.\n\n\n\n"
        "Examples:\n\n"
        "--hook-variable 'name=\"app id\",type=integer,required=true'\n\n"
        '--hook-variable \'name="env",type=string,default_value="production"\'\n\n'
        '--hook-variable \'name="regions",type=array,default_value="[\\"us-east-1\\",\\"eu-west-1\\"]"\'\n\n',  # noqa: E501
    ),
) -> None:
    """Create a hook for a pipeline."""

    # Combine multiple HookTriggerWhen into a single one
    parsed_hook_trigger_when = HookTriggerWhen(
        events=[e for tw in hook_trigger_when for e in tw.events],  # type: ignore
        conditions=[c for tw in hook_trigger_when for c in tw.conditions],  # type: ignore
    )

    res = devopness.hooks.add_pipeline_hook(
        "incoming",
        pipeline_id,
        HookPipelineCreate(
            name=hook_name,
            requires_secret=hook_requires_secret,
            trigger_when=parsed_hook_trigger_when,
            settings=HookIncomingSettings(
                variables=hook_variables,
            ),
        ),
    )

    hook = res.data

    def format_trigger_when(hook: Hook) -> Panel:
        """
        Returns a Rich renderable object showing hook.trigger_when details
        with nested panels for Events and Conditions.
        """

        events = hook.trigger_when.events or []
        conditions = hook.trigger_when.conditions or []

        # --- Events block ---
        if events:
            events_content = "\n".join(f"• [cyan]{e}[/cyan]" for e in events)
        else:
            events_content = "[dim]- None[/dim]"

        events_panel = Panel(
            events_content,
            title="[bold underline]Events[/bold underline]",
            border_style="cyan",
            padding=(0, 1),
        )

        # --- Conditions block ---
        if conditions:
            cond_blocks = []
            for c in conditions:
                values = (
                    ", ".join(f"[green]{v}[/green]" for v in (c.accepted_values or []))
                    if c.accepted_values
                    else "[dim]None[/dim]"
                )
                cond_blocks.append(
                    f"[bold]Path:[/bold] [cyan]{c.path}[/cyan]\n"
                    f"[bold]Accepted Values:[/bold] {values}"
                )

            conditions_content = "\n\n".join(cond_blocks)
        else:
            conditions_content = "[dim]- None[/dim]"

        conditions_panel = Panel(
            conditions_content,
            title="[bold underline]Conditions[/bold underline]",
            border_style="magenta",
            padding=(0, 1),
        )

        # Combine both sections
        return Panel.fit(
            title="Trigger When",
            renderable=Group(events_panel, conditions_panel),
        )

    def format_hook_variables(hook: Hook) -> Group | str:
        """
        Format hook.settings.variables as a Rich renderable (Group of Panels).
        Each variable is displayed inside its own panel with colored labels.
        """

        variables = getattr(hook.settings, "variables", []) or []

        if not variables:
            return "[dim]- No variables defined[/dim]"

        panels = []

        for var in variables:
            name = f"[cyan]{var.name or '-'}[/cyan]"
            path = f"[cyan]{var.path or var.name or '-'}[/cyan]"
            vtype = f"[magenta]{var.type or '-'}[/magenta]"
            required = (
                "[green]Yes[/green]"
                if var.required
                else "[red]No[/red]"
                if var.required is not None
                else "[dim]None[/dim]"
            )

            # Pretty-print default_value (stringify lists/dicts nicely)
            if isinstance(var.default_value, (list, dict)):
                default_value = f"[white]{var.default_value}[/white]"

            elif var.default_value is None:
                default_value = "[dim]None[/dim]"

            else:
                default_value = f"[white]{var.default_value}[/white]"

            panels.append(
                Panel(
                    f"[bold]Name:[/bold] {name}\n"
                    f"[bold]Path:[/bold] {path}\n"
                    f"[bold]Type:[/bold] {vtype}\n"
                    f"[bold]Required:[/bold] {required}\n"
                    f"[bold]Default Value:[/bold] {default_value}",
                    title=f"[bold underline]{var.name or 'Variable'}[/bold underline]",
                    border_style="cyan",
                    padding=(0, 1),
                )
            )

        return Group(*panels)

    return details(
        data=hook,
        resource_id=hook.id,
        resource_name="Hook",
        fullscreen=True,
        rows=[
            DetailsRow[Hook](
                header="ID",
                get_value=lambda p: str(p.id),
            ),
            DetailsRow[Hook](
                header="Name",
                get_value=lambda p: p.name,
            ),
            DetailsRow.line(),
            DetailsRow[Hook](
                header="Trigger When",
                get_value=format_trigger_when,  # type: ignore
            ),
            DetailsRow[Hook](
                header="Settings",
                get_value=format_hook_variables,  # type: ignore
            ),
            DetailsRow.line(),
        ],
    )
