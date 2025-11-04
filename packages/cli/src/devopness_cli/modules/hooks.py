import json
import shlex
from typing import List, Union, cast

import click
import typer
from devopness.models import (
    Hook,
    HookIncomingSettingsPlain,
    HookPipelineCreatePlain,
    HookPipelineCreateSettings,
    HookPipelineCreateSettingsPlain,
    HookRelation,
    HookTypeParam,
    HookTypeParamPlain,
    HookVariable,
    HookVariableType,
    HookIncomingSettings,
    HookPipelineCreate,
    HookTriggerWhen,
)
from rich.console import Console

import devopness_cli.types as types
from devopness_cli.components.details import DetailsRow, details
from devopness_cli.components.summary import SummaryColumn, summary
from devopness_cli.components.to_json import to_json
from devopness_cli.services.devopness_api import devopness

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
    res = devopness.hooks.add_pipeline_hook(
        "incoming",
        pipeline_id,
        HookPipelineCreate(
            name=hook_name,
            requires_secret=hook_requires_secret,
            trigger_when=HookTriggerWhen(
                conditions=[],
            ),
            settings=HookIncomingSettings(
                variables=hook_variables,
            ),
        ),
    )

    hook = res.data

    return details(
        data=hook,
        resource_id=hook.id,
        resource_name="Hook",
        rows=[
            DetailsRow[Hook](
                header="ID",
                get_value=lambda p: str(p.id),
            ),
            DetailsRow[Hook](
                header="Name",
                get_value=lambda p: p.name,
            ),
        ],
    )
