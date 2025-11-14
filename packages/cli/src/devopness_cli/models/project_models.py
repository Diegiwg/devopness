from dataclasses import dataclass

from cyclopts import Parameter


@Parameter(name="*")
@dataclass
class ProjectCreateModel:
    """
    Project create model.

    Attributes:
        name (str): The name of the project.
    """

    name: str
