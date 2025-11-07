from cyclopts import App

from devopness_cli.commands import register_commands


def main() -> None:
    """Entry point for the Devopness CLI."""

    app = App(
        help="Devopness CLI - Painless essential DevOps to everyone",
    )

    register_commands(app)

    app()

if __name__ == "__main__":
    main()
