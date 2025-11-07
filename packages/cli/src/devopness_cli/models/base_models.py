from dataclasses import dataclass
from typing import Literal

from cyclopts import Parameter


@Parameter(name="*")
@dataclass
class BasePageModel:
    """
    Base model for pagination options.

    Attributes:
        page (int): The page number.
        per_page (int): The number of items per page.
    """

    page: int = 1
    per_page: int = 20


@Parameter(name="*")
@dataclass
class BaseOutputModel:
    """
    Base model for output options.

    Attributes:
        format (Literal["table", "json", "plain"]): The output format.
    """

    format: Literal["table", "json", "plain"] = "table"
