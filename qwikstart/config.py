from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

BUILTIN_GIT_ABBREVIATIONS = {
    "gh": "https://github.com/{0}",
    "gl": "https://gitlab.com/{0}",
    "bb": "https://bitbucket.org/{0}",
}


def _make_default_git_abbrev() -> Dict[str, str]:
    return BUILTIN_GIT_ABBREVIATIONS


@dataclass(frozen=True)
class Config:
    qwikstart_cache: Path = Path("~/.qwikstart/cached_repos").expanduser()
    git_abbreviations: Dict[str, str] = field(default_factory=_make_default_git_abbrev)

    def ensure_cache_directory_exists(self) -> None:
        self.qwikstart_cache.mkdir(parents=True, exist_ok=True)


def get_user_config() -> Config:
    return Config()
