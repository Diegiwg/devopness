from typer.main import Typer

import devopness_cli_with_typer.modules.applications as applications
import devopness_cli_with_typer.modules.config as config
import devopness_cli_with_typer.modules.environments as environments
import devopness_cli_with_typer.modules.hooks as hooks
import devopness_cli_with_typer.modules.pipelines as pipelines
import devopness_cli_with_typer.modules.projects as projects

MODULES: list[tuple[str, Typer]] = [
    ("project", projects.app),
    ("environment", environments.app),
    ("application", applications.app),
    ("pipeline", pipelines.app),
    ("hook", hooks.app),
    ("config", config.app),
]
