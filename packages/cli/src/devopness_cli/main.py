import typer

import devopness_cli.modules.projects as projects

app = typer.Typer(help="Devopness CLI Tool")

app.add_typer(
    projects.app,
    name="projects",
    )


def main() -> None:
    """Runs the Devopness CLI Tool."""

    app()


if __name__ == "__main__":
    main()
