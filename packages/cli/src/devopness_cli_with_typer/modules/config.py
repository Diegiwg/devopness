import typer
from rich.console import Console
from rich.table import Table

from devopness_cli_with_typer.services.config_manage import Config, ConfigManager

app = typer.Typer(
    name="config",
    help="Manage Devopness CLI configuration.",
    no_args_is_help=True,
)

console = Console()


@app.command(name="init")
def init_config() -> None:
    """Interactively initialize configuration."""

    # Set Base URL
    base_url = typer.prompt(
        "Enter the Devopness API Base URL",
        default="https://api.devopness.com",
    )

    if not Config.validate_url(base_url):
        raise typer.BadParameter("Base URL must start with http:// or https://")

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


@app.command(name="set")
def set_config(
    token: str = typer.Option(
        default=None,
        help="Personal Access Token for authentication.",
        hide_input=True,
    ),
    base_url: str = typer.Option(
        default=None,
        help="Base URL for the Devopness API.",
    ),
) -> None:
    """Set configuration options non-interactively."""

    if not token and not base_url:
        console.print("[yellow]No changes provided.[/yellow]")

        return

    cfg = ConfigManager.load()

    if token:
        cfg.token = token

    if base_url:
        if not Config.validate_url(base_url):
            raise typer.BadParameter("Base URL must start with http:// or https://")

        cfg.base_url = base_url

    ConfigManager.save(cfg)

    console.print("[green]Configuration has been updated successfully.[/green]")


@app.command(name="show")
def show_config() -> None:
    """Display current Devopness CLI configuration."""
    cfg = ConfigManager.load()

    table = Table(
        box=None,
        show_header=False,
    )

    table.add_row(
        "[bold cyan]API URL[/bold cyan]",
        cfg.base_url,
    )

    table.add_row(
        "[bold cyan]Token is configured[/bold cyan]",
        "Yes" if cfg.token else "No",
    )

    table.add_row(
        "[bold cyan]Config file location[/bold cyan]",
        str(cfg.location),
    )

    console.print(table)


@app.command(name="clear")
def clear_config() -> None:
    """Clear the stored API token."""
    ConfigManager.clear()

    console.print("[green]Configuration has been cleared successfully.[/green]")
