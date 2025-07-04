"""
Devopness API Python SDK - Painless essential DevOps to everyone

Note:
    This is auto generated by OpenAPI Generator.
    https://openapi-generator.tech
"""

import json
from enum import Enum
from typing import Literal, Self


class NetworkRuleDirection(str, Enum):
    """
    The direction of network traffic a network rule is applied. `Inbound` applies to ingress/incoming traffic originating from outside into your network. `Outbound` applies to egress traffic, originating inside your network to external networks.
    """

    INBOUND = "inbound"
    OUTBOUND = "outbound"

    def __str__(self) -> str:
        """Return the string representation of the NetworkRuleDirection"""
        return self.value

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of NetworkRuleDirection from a JSON string"""
        return cls(json.loads(json_str))


# The plain version of NetworkRuleDirection
NetworkRuleDirectionPlain = Literal[
    "inbound",
    "outbound",
]
