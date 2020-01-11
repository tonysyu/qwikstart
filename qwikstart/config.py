from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    qwikstart_cache: Path = Path("~/.qwikstart/cached_repos").expanduser()

    def ensure_cache_directory_exists(self) -> None:
        self.qwikstart_cache.mkdir(parents=True, exist_ok=True)


def get_user_config() -> Config:
    return Config()
