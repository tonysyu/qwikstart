#!/usr/bin/env python3
import textwrap

import click

from ..parser import get_operations_mapping
from ..utils import logging
from .resolver import resolve_task
from .utils import ContextVar, get_operation_help


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
    op_help = get_operation_help(op_name)

    echo_field(op_name, op_help.docstring, color="green")

    if op_help.required_context:
        click.echo(f"\nRequired context:")
    for context_var in op_help.required_context:
        echo_context_var(context_var)

    if op_help.required_context:
        click.echo(f"\nOptional context:")
    for context_var in op_help.optional_context:
        echo_context_var(context_var)


def echo_context_var(context_var: ContextVar):
    click.secho(context_var.name, fg="green")
    echo_field(indent("type"), context_var.annotation)
    if not context_var.is_required:
        echo_field(indent("default"), context_var.default)
    if context_var.description:
        click.echo(indent(context_var.description))


def indent(text, level=1):
    prefix = "    " * level
    return textwrap.indent(text, prefix)


def echo_field(field_name, field_value, color="yellow"):
    click.echo(click.style(field_name, fg=color) + f": {field_value}")


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
