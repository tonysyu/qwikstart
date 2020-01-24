from unittest.mock import Mock, patch

import pytest
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart import config
from qwikstart.exceptions import ConfigurationError

DEFAULT_CONFIG = config.Config(**config.DEFAULT_CONFIG_DICT)


@patch.object(config, "load_custom_config_file")
class TestGetUserConfig:
    def test_empty_config_file(self, mock_load_file: Mock) -> None:
        mock_load_file.return_value = {}
        assert config.get_user_config() == DEFAULT_CONFIG

    def test_override_qwikstart_cache(self, mock_load_file: Mock) -> None:
        mock_load_file.return_value = {"qwikstart_cache": "fake/path/to/cache"}
        user_config = config.get_user_config()
        assert user_config.qwikstart_cache == "fake/path/to/cache"

    def test_add_git_abbreviation(self, mock_load_file: Mock) -> None:
        mock_load_file.return_value = {
            "git_abbreviations": {"new": "https://git.example.com/{0}"}
        }
        user_config = config.get_user_config()
        assert user_config.git_abbreviations == {
            "gh": "https://github.com/{0}",
            "gl": "https://gitlab.com/{0}",
            "bb": "https://bitbucket.org/{0}",
            "new": "https://git.example.com/{0}",
        }

    def test_overwrite_git_abbreviation(self, mock_load_file: Mock) -> None:
        mock_load_file.return_value = {
            "git_abbreviations": {"gh": "https://---FAKE---.github.com/{0}"}
        }
        user_config = config.get_user_config()
        assert user_config.git_abbreviations == {
            "gh": "https://---FAKE---.github.com/{0}",
            "gl": "https://gitlab.com/{0}",
            "bb": "https://bitbucket.org/{0}",
        }

    @patch.object(config, "logger")
    def test_unknown_config_key(self, mock_logger: Mock, mock_load_file: Mock) -> None:
        mock_load_file.return_value = {"unknown_config": "fake-value"}
        assert config.get_user_config() == DEFAULT_CONFIG
        mock_logger.warning.assert_called_once()


class TestLoadUserConfigFile(TestCase):
    def setUp(self) -> None:
        # Reload `config` module since it defines global Paths that need to be patched.
        # See https://jmcgeheeiv.github.io/pyfakefs/release/usage.html#modules-to-reload
        self.setUpPyfakefs(modules_to_reload=[config])

    def test_file_does_not_exist_gives_empty_custom_config(self) -> None:
        assert config.load_custom_config_file() == {}

    def test_empty_file_gives_empty_custom_config(self) -> None:
        self.fs.create_file(config.QWIKSTART_CONFIG_FILE, contents="")
        assert config.load_custom_config_file() == {}

    def test_simple_dict_loaded(self) -> None:
        self.fs.create_file(config.QWIKSTART_CONFIG_FILE, contents="key: value")
        assert config.load_custom_config_file() == {"key": "value"}

    def test_top_level_list_raises_an_error(self) -> None:
        self.fs.create_file(config.QWIKSTART_CONFIG_FILE, contents="- key: value")
        error_msg = "Expected .* to contain a dictionary."
        with pytest.raises(ConfigurationError, match=error_msg):
            assert config.load_custom_config_file()
