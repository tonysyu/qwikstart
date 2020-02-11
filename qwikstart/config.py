import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from . import utils
from .exceptions import ConfigurationError
from .utils import io

logger = logging.getLogger(__name__)

QWIKSTART_CONFIG_FILE = Path("~/.qwikstart/config.yml").expanduser()

DEFAULT_CONFIG_DICT: Dict[str, Any] = {
    "repo_cache": "~/.qwikstart/cached_repos",
    "git_abbreviations": {
        "gh": "https://github.com/{0}",
        "gl": "https://gitlab.com/{0}",
        "bb": "https://bitbucket.org/{0}",
    },
}


@dataclass(frozen=True)
class Config:
    repo_cache: str
    git_abbreviations: Dict[str, str]

    @property
    def repo_cache_path(self) -> Path:
        return Path(self.repo_cache).expanduser()


def get_user_config() -> Config:
    user_config = load_custom_config_file()
    known_config_keys = set(utils.get_dataclass_keys(Config))

    unknown_config_keys = set(user_config).difference(known_config_keys)
    if unknown_config_keys:
        logger.warning(
            f"User config, {QWIKSTART_CONFIG_FILE}, contains unknown keys: "
            "{unknown_config_keys}. Ignoring extra keys."
        )
        user_config = {k: v for k, v in user_config.items() if k in known_config_keys}

    return Config(**utils.merge_nested_dicts(DEFAULT_CONFIG_DICT, user_config))


def load_custom_config_file() -> Dict[str, Any]:
    if QWIKSTART_CONFIG_FILE.exists():
        logger.debug(f"Loading user config from {QWIKSTART_CONFIG_FILE}")
        user_config = io.load_yaml_file(QWIKSTART_CONFIG_FILE)

        if not user_config:
            return {}

        if not isinstance(user_config, dict):
            msg = f"Expected {QWIKSTART_CONFIG_FILE} to contain a dictionary."
            raise ConfigurationError(msg)

        return user_config

    logger.debug(f"No user config found at {QWIKSTART_CONFIG_FILE}")
    return {}
