from devopness import DevopnessClient, DevopnessClientConfig

from devopness_cli.services.config_manage import ConfigManager

cfg = ConfigManager.load()

devopness = DevopnessClient(
    DevopnessClientConfig(
        base_url=cfg.base_url,
        auto_refresh_token=False,
        api_token=cfg.token,
    )
)
