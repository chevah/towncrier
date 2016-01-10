# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
towncrier, a builder for your news files.
"""

from __future__ import absolute_import, division

import os
import click

from datetime import date

from collections import OrderedDict

from ._settings import load_config
from ._builder import find_fragments, split_fragments, render_fragments
from ._project import get_version, get_project_name
from ._writer import append_to_newsfile
from ._git import remove_files, stage_newsfile


def _get_date():
    return date.today().isoformat()


@click.command()
@click.option('--draft', 'draft', default=False, flag_value=True,
              help=("Render the news fragments, don't write to files, "
                    "don't check versions."))
@click.option('--dir', 'directory', default='.')
@click.option('--version', 'project_version', default=None)
@click.option('--date', 'project_date', default=None)
@click.option(
    '--package', 'package', default=None,
    help='Name of the package for which to detect the version',
    )
@click.option(
    '--filename', 'filename', default=None,
    help='Path to the files which is updated.',
    )
@click.option(
    '--yes', 'yes', default=False, flag_value=True,
    help='Assume fragment files are removed from git.',
    )
def _main(
        draft, directory, project_version, project_date, filename, package,
        yes):
    return __main(
        draft, directory, project_version, project_date, filename, package,
        yes)


def __main(
        draft, directory, project_version, project_date, filename, package, yes
        ):
    """
    The main entry point.
    """
    directory = os.path.abspath(directory)

    config = {
        'package': package,
        'package_dir': '.',
        'filename': filename,
        'sections': {'': ''},
    }

    click.echo("Finding news fragments...")

    # TODO make these customisable
    # ('Section Name', include_text, include_ticket)
    definitions = OrderedDict([
        ("feature", ("New Features", True, False)),
        ("bugfix", ("Defect Fixes", True, True)),
        ("removal", ("Deprecations and Removals", True, True)),
        ("misc", ("Misc", False, False)),
    ])

    fragments = find_fragments(directory, config['sections'])

    click.echo("Rendering news fragments...")

    fragments = split_fragments(fragments, definitions)
    rendered = render_fragments(fragments, definitions)

    if not project_version:
        project_version = get_version(
            os.path.join(directory, config['package_dir']),
            config['package'])

    project_name = get_project_name(
        os.path.join(directory, config['package_dir']),
        config['package'])

    name_and_version = "Version " + project_version

    if project_date is None:
        project_date = _get_date()

    if project_date != "":
        name_and_version += ", " + project_date

    if draft:
        click.echo("Draft only -- nothing has been written.")
        click.echo("What is seen below is what would be written.\n")
        click.echo(name_and_version)
        click.echo("=" * len(name_and_version) + "\n")
        click.echo(rendered)
    else:
        click.echo("Writing to newsfile...")
        append_to_newsfile(directory, config['filename'],
                           name_and_version, rendered)

        click.echo("Staging newsfile...")
        stage_newsfile(directory, config['filename'])

        click.echo("Removing news fragments...")
        remove_files(directory, config['package_dir'],
                     config['package'], config['sections'], fragments, yes)

        click.echo("Done!")


from ._version import __version__

__all__ = ["__version__"]
