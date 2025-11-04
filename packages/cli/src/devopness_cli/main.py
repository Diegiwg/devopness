import typer

from devopness_cli.modules import MODULES

app = typer.Typer(
    name="Devopness CLI Tool",
    help="Command-line interface for Devopness platform.",
    no_args_is_help=True,
)

for module_name, module_app in MODULES:
    app.add_typer(module_app, name=module_name)


def main() -> None:
    """Runs the Devopness CLI Tool."""

    app()


if __name__ == "__main__":
    main()
