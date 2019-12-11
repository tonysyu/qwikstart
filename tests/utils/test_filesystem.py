import os
from pathlib import Path

import jinja2
from pyfakefs.fake_filesystem_unittest import TestCase  # type: ignore

from qwikstart.utils import filesystem, templates


class TestRenderFileTree(TestCase):
    source_dir = Path("/source")
    target_dir = Path("/target")

    def setUp(self):
        self.setUpPyfakefs()
        self.fs.create_dir(self.source_dir)
        self.fs.create_dir(self.target_dir)

    def render_source_directory_to_target_directory(
        self, template_variables=None
    ) -> None:
        renderer = templates.TemplateRenderer(
            jinja2.FileSystemLoader("/"), template_variables=template_variables
        )
        filesystem.render_file_tree(self.source_dir, self.target_dir, renderer)

    def test_empty_source_tree(self):
        self.render_source_directory_to_target_directory()
        assert os.listdir(self.target_dir) == []

    def test_copy_single_file(self):
        self.fs.create_file(self.source_dir / "test.txt", contents="test")
        self.render_source_directory_to_target_directory()

        assert os.listdir(self.target_dir) == ["test.txt"]
        with open(self.target_dir / "test.txt") as f:
            assert f.read() == "test"

    def test_copy_file_in_directory(self):
        directory = self.source_dir / "subdir"
        self.fs.create_dir(directory)
        self.fs.create_file(directory / "test.txt")
        self.render_source_directory_to_target_directory()

        assert os.path.isdir(self.target_dir / "subdir")
        assert os.path.isfile(self.target_dir / "subdir" / "test.txt")

    def test_render_variable_in_directory_name(self):
        directory = self.source_dir / "{{ qwikstart.name }}"
        self.fs.create_dir(directory)
        self.render_source_directory_to_target_directory(
            template_variables={"name": "dynamic-name"}
        )

        assert os.path.isdir(self.target_dir / "dynamic-name")

    def test_render_variable_in_file_name(self):
        self.fs.create_file(self.source_dir / "{{ qwikstart.name }}.txt")
        self.render_source_directory_to_target_directory(
            template_variables={"name": "dynamic-name"}
        )

        assert os.path.isfile(self.target_dir / "dynamic-name.txt")

    def test_render_variable_in_file_contents(self):
        self.fs.create_file(
            self.source_dir / "test.txt",
            contents="Hello, {{ qwikstart.name }}!",
        )
        self.render_source_directory_to_target_directory(
            template_variables={"name": "World"}
        )

        with open(self.target_dir / "test.txt") as f:
            assert f.read() == "Hello, World!"
