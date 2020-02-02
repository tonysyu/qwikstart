"""
Tests for qwikstart.utils.filesystem

These tests use pyfakefs (https://jmcgeheeiv.github.io/pyfakefs/) for mocking
the filesystem. It appears that this doesn't play nicely with `ipdb` so any
debugging of these tests will need to be done with normal `pdb`.
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import jinja2
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.utils import filesystem, templates


class TestRenderFileTree(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

        # Define paths here rather than using class variables since pyfakefs
        # can't patch globally scoped variables.
        self.source_dir = Path("/source")
        self.target_dir = Path("/target")

        self.fs.create_dir(self.source_dir)
        self.fs.create_dir(self.target_dir)

    def render_source_directory_to_target_directory(
        self,
        template_variables: Optional[Dict[str, Any]] = None,
        source_dir: Optional[Path] = None,
        target_dir: Optional[Path] = None,
        ignore_patterns: Optional[List[str]] = None,
    ) -> None:
        renderer = templates.TemplateRenderer(
            jinja2.FileSystemLoader("/"), template_variables=template_variables
        )
        generator = filesystem.FileTreeGenerator(
            source_dir or self.source_dir,
            target_dir or self.target_dir,
            renderer,
            ignore_patterns or [],
        )
        generator.copy()

    def test_empty_source_tree(self) -> None:
        self.render_source_directory_to_target_directory()
        assert os.listdir(self.target_dir) == []

    def test_copy_single_file(self) -> None:
        self.fs.create_file(self.source_dir / "test.txt", contents="test")
        self.render_source_directory_to_target_directory()

        assert os.listdir(self.target_dir) == ["test.txt"]
        with open(self.target_dir / "test.txt") as f:
            assert f.read() == "test"

    def test_copy_binary_file(self) -> None:
        data = bytes([123, 3, 255, 0, 100])
        with open(self.source_dir / "array.bin", "wb") as f:
            assert f.write(data)
        self.render_source_directory_to_target_directory()

        assert os.listdir(self.target_dir) == ["array.bin"]
        with open(self.target_dir / "array.bin", "rb") as f:
            assert f.read() == data

    def test_copy_file_in_directory(self) -> None:
        subdir = self.source_dir / "subdir"
        self.fs.create_dir(subdir)
        self.fs.create_file(subdir / "test.txt")
        self.render_source_directory_to_target_directory()

        assert os.path.isdir(self.target_dir / "subdir")
        assert os.path.isfile(self.target_dir / "subdir" / "test.txt")

        # Regression test: Previous versions copied subdirectory files
        # to the parent directory in addition to the subdirectory.
        assert not os.path.isfile(self.target_dir / "test.txt")

    def test_create_target_directory(self) -> None:
        self.fs.create_file(self.source_dir / "test.txt")
        target_dir = self.target_dir / "subdir"
        assert not os.path.isdir(target_dir)
        self.render_source_directory_to_target_directory(target_dir=target_dir)

        assert os.path.isdir(self.target_dir / "subdir")
        assert os.path.isfile(self.target_dir / "subdir" / "test.txt")

    def test_render_variable_in_directory_name(self) -> None:
        subdir = self.source_dir / "{{ qwikstart.name }}"
        self.fs.create_dir(subdir)
        self.fs.create_file(subdir / "test.txt")

        self.render_source_directory_to_target_directory(
            template_variables={"name": "dynamic-name"}
        )

        assert os.path.isdir(self.target_dir / "dynamic-name")
        assert os.path.isfile(self.target_dir / "dynamic-name" / "test.txt")

    def test_render_variable_in_file_name(self) -> None:
        self.fs.create_file(self.source_dir / "{{ qwikstart.name }}.txt")
        self.render_source_directory_to_target_directory(
            template_variables={"name": "dynamic-name"}
        )

        assert os.path.isfile(self.target_dir / "dynamic-name.txt")

    def test_render_sub_directory(self) -> None:
        subdir = self.source_dir / "subdir"
        self.fs.create_dir(subdir)
        self.fs.create_file(subdir / "test.txt")
        self.render_source_directory_to_target_directory(source_dir=subdir)

        # Only the contents of subdir should be copied, not subdir itself.
        assert not os.path.exists(self.target_dir / "subdir")
        assert os.path.isfile(self.target_dir / "test.txt")

    def test_render_variable_in_file_contents(self) -> None:
        self.fs.create_file(
            self.source_dir / "test.txt", contents="Hello, {{ qwikstart.name }}!"
        )
        self.render_source_directory_to_target_directory(
            template_variables={"name": "World"}
        )

        with open(self.target_dir / "test.txt") as f:
            assert f.read() == "Hello, World!"

    def test_ignore_single_file(self) -> None:
        self.fs.create_file(self.source_dir / "ignore.txt")
        self.render_source_directory_to_target_directory(ignore_patterns=["ignore.txt"])

        assert not os.listdir(self.target_dir)

    def test_ignore_file_in_sub_directory(self) -> None:
        self.fs.create_file(self.source_dir / "subdirectory/ignore.txt")
        self.render_source_directory_to_target_directory(
            ignore_patterns=["subdirectory/ignore.txt"]
        )
        assert os.listdir(self.target_dir) == ["subdirectory"]


class TestFnmatchesToRegex:
    def test_exact_match(self) -> None:
        pattern = filesystem.fnmatches_to_regex(["exact-match"])
        assert pattern.match("exact-match")
        assert not pattern.match("match")
        assert not pattern.match("exact")

    def test_matches_one_of_two(self) -> None:
        pattern = filesystem.fnmatches_to_regex(["one", "two"])
        assert pattern.match("one")
        assert pattern.match("two")

    def test_match_any_in_directory(self) -> None:
        pattern = filesystem.fnmatches_to_regex([r"match_dir/*"])
        assert pattern.match("match_dir/fake.txt")

    def test_match_file_extension(self) -> None:
        pattern = filesystem.fnmatches_to_regex([r"*.txt"])
        assert pattern.match("match.txt")
        assert not pattern.match("ignore.py")

    def test_empty_list_should_not_match_anything(self) -> None:
        pattern = filesystem.fnmatches_to_regex([])
        assert not pattern.match("")
        assert not pattern.match("hello")
