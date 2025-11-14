from cyclopts import App


def register_commands(app: App) -> None:
    """Register CLI commands."""
    from .project_command import Project  # noqa: PLC0415

    app.command(Project)
