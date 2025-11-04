import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import keyring
import typer

APP_NAME = "devopness_cli"
CONFIG_DIR = Path(typer.get_app_dir(APP_NAME))
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    """Represents the CLI configuration."""

    base_url: str = "https://api.devopness.com"
    token: str | None = None  # token is not stored in plain text

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate a URL by checking if it starts with http:// or https://.
        """
        return re.match(r"^https?://", url) is not None


class ConfigManager:
    """Handles secure loading and saving of CLI configuration."""

    @staticmethod
    def load() -> Config:
        """Load configuration from file and keyring."""
        data = {}

        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        token = keyring.get_password(APP_NAME, "token")

        config = Config(token=token, **data)

        if not config.validate_url(config.base_url):
            config.base_url = "https://api.devopness.com"

        return config

    @staticmethod
    def save(config: Config) -> None:
        """Save configuration safely (secure token handling)."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        # Save only non-sensitive data to the config file
        data = asdict(config).copy()
        data.pop("token", None)

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Store sensitive data (token) in OS keyring
        if config.token:
            keyring.set_password(APP_NAME, "token", config.token)

    @staticmethod
    def clear() -> None:
        """Remove stored token from keyring and config file."""
        keyring.delete_password(APP_NAME, "token")

        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
