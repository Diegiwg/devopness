from typer.main import Typer

import devopness_cli.modules.config as config
import devopness_cli.modules.environments as environments
import devopness_cli.modules.projects as projects

MODULES: list[tuple[str, Typer]] = [
    ("projects", projects.app),
    ("environments", environments.app),
    ("config", config.app),
]
