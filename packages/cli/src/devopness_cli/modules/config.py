import typer
from rich.console import Console

from devopness_cli.services.config_manage import ConfigManager

app = typer.Typer(
    name="config",
    help="Manage Devopness CLI configuration.",
    no_args_is_help=True,
)

set_app = typer.Typer(
    name="set",
    help="Set configuration values.",
    no_args_is_help=True,
)

app.add_typer(set_app, name="set")

console = Console()


@app.command(name="init")
def init_config() -> None:
    """Interactively initialize configuration."""

    # Set Base URL
    base_url = typer.prompt(
        "Enter the Devopness API Base URL",
        default="https://api.devopness.com",
    )

    # Set API Token
    token = typer.prompt(
        "Enter your Devopness API Token",
        hide_input=True,
    )

    cfg = ConfigManager.load()
    cfg.base_url = base_url
    cfg.token = token

    ConfigManager.save(cfg)

    console.print("[green]Configuration has been initialized successfully.[/green]")


@app.command(name="show")
def show_config() -> None:
    """Display current configuration."""
    cfg = ConfigManager.load()

    console.print(f"[bold]API URL:[/bold] {cfg.base_url}")
    console.print(f"[bold]Token is configured:[/bold] {'Yes' if cfg.token else 'No'}")


@app.command(name="clear")
def clear_token() -> None:
    """Clear the stored API token."""
    ConfigManager.clear_token()

    console.print("[green]Token has been cleared successfully.[/green]")


@set_app.command(name="token")
def set_token(
    token: str = typer.Option(
        help="Personal Access Token for authentication.",
        prompt=True,
        hide_input=True,
        prompt_required=False,
    ),
) -> None:
    """Set the API token for authentication."""

    cfg = ConfigManager.load()
    cfg.token = token

    ConfigManager.save(cfg)

    console.print("[green]Token has been set successfully.[/green]")


@set_app.command(name="base-url")
def set_base_url(
    base_url: str = typer.Option(
        help="Base URL for the Devopness API.",
        prompt=True,
        prompt_required=False,
    ),
) -> None:
    """Set the base URL for the Devopness API."""

    cfg = ConfigManager.load()
    cfg.base_url = base_url

    ConfigManager.save(cfg)

    console.print("[green]Base URL has been set successfully.[/green]")
