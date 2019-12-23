#!/usr/bin/env python3
import click

from ..parser import get_operations_mapping
from ..utils import logging
from .resolver import resolve_task


@click.group()
def cli():
    pass


@cli.command()
@click.argument("task_path")
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Print debug information",
    default=False,
)
def run(task_path, verbose):
    """Run task in the current directory."""
    logging.configure_logger("DEBUG" if verbose else "INFO")
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
    variables.pop("execution_context", None)
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
