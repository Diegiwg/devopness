from typer.main import Typer

import devopness_cli.modules.applications as applications
import devopness_cli.modules.config as config
import devopness_cli.modules.environments as environments
import devopness_cli.modules.projects as projects

MODULES: list[tuple[str, Typer]] = [
    ("project", projects.app),
    ("environment", environments.app),
    ("application", applications.app),
    ("config", config.app),
]
