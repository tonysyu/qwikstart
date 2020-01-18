"""
Tests for qwikstart.utils.templates

These tests use pyfakefs (https://jmcgeheeiv.github.io/pyfakefs/) for mocking
the filesystem. It appears that this doesn't play nicely with `ipdb` so any
debugging of these tests will need to be done with normal `pdb`.
"""
from pathlib import Path
from typing import Any, Dict, Optional

import jinja2
from pyfakefs.fake_filesystem_unittest import TestCase

from qwikstart.utils import templates


class TestRenderFileTree(TestCase):
    def setUp(self) -> None:
        self.setUpPyfakefs()

        # Define paths here rather than using class variables since pyfakefs
        # can't patch globally scoped variables.
        self.source_dir = Path("/source")
        self.fs.create_dir(self.source_dir)

    def get_template_renderer(
        self, template_variables: Optional[Dict[str, Any]] = None
    ) -> templates.TemplateRenderer:
        return templates.TemplateRenderer(
            jinja2.FileSystemLoader("/"), template_variables=template_variables
        )

    def test_render(self) -> None:
        template_path = self.source_dir / "test.txt"
        self.fs.create_file(template_path, contents="test")
        renderer = self.get_template_renderer()
        assert renderer.render(str(template_path)) == "test"

    def test_get_template_path_is_resolved(self) -> None:
        # This is a regression test for unresolved paths, which jinja2's
        # `FileSystemLoader` does not resolve..
        template_path = self.source_dir / "../source/test.txt"
        self.fs.create_file(template_path)
        renderer = self.get_template_renderer()
        assert isinstance(renderer.get_template(str(template_path)), jinja2.Template)

    def test_meta_variables(self) -> None:
        renderer = self.get_template_renderer()
        renderer.template_variables = {
            templates.TEMPLATE_VARIABLE_META_PREFIX: {
                "target_dir": Path("."),
                "source_dir": self.source_dir,
            }
        }
