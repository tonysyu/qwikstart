#!/usr/bin/env python3
from pathlib import Path
from typing import Any, Dict, Optional

import click
import yaml

from .parser import ParserError, get_operations_mapping, parse_task


class YamlLoader:
    known_extensions = {".yaml", ".yml"}

    def can_handle(self, file_path: Path) -> bool:
        return file_path.suffix in self.known_extensions

    def load(self, file_path: Path) -> Dict[str, Any]:
        with open(file_path) as f:
            return yaml.safe_load(f)


loaders_list = [YamlLoader()]


class ResolveLocalPath:
    def __init__(self, path: str, root: Path = None):
        root = root or Path(".")
        self.resolved_path = root.joinpath(path).resolve()

    def exists(self) -> bool:
        return self.resolved_path.is_file()

    def parsed_data(self) -> Dict[str, Any]:
        for loader in loaders_list:
            if loader.can_handle(self.resolved_path):
                return loader.load(self.resolved_path)
        else:
            raise RuntimeError(f"No loader to handle {self.resolved_path!r}")


task_resolver_list = [ResolveLocalPath]


def resolve_task(task_path):
    attempted_paths = []
    for path_resolver in task_resolver_list:
        resolver = path_resolver(task_path)
        if resolver.exists():
            return parse_task(resolver.parsed_data(), resolver.resolved_path)
        else:
            attempted_paths.append(resolver.resolved_path)
    else:
        attempts = "\n- ".join(attempted_paths)
        raise RuntimeError(f"Could not resolve path. Attempted: {attempts}")


@click.group()
def cli():
    pass


@cli.command()
@click.argument("task_path")
def run(task_path):
    """Run task in the current directory."""
    task = resolve_task(task_path)
    task.execute()


@cli.command()
@click.argument("op_name")
def help(op_name):
    """Show help for the given operation."""
    op_mapping = get_operations_mapping()
    operation = op_mapping[op_name]

    click.echo(click.style(op_name, fg="green") + f": {operation.__doc__}")

    variables = operation.run.__annotations__["context"].__annotations__
    if variables:
        click.echo(f"\nContext variables:")
    for var_name, var_type in variables.items():
        click.echo(click.style(var_name, fg="yellow") + f": {var_type}")


@cli.command()
def list_operations():
    """Show help for the given operation."""
    op_mapping = get_operations_mapping()
    for op_name, operation in op_mapping.items():
        click.echo(click.style(op_name, fg="green") + f": {operation.__doc__}")


def main():
    cli()


if __name__ == "__main__":
    cli()
