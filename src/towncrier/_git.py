# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

from subprocess import call

import os
import click


def remove_files(directory, package_dir, package, sections, fragments, yes):

    base_dir = directory

    to_remove = []

    for section_name, categories in fragments.items():

        section_dir = os.path.join(base_dir, "release-notes",
                                   sections[section_name])

        for category_name, category_items in categories.items():

            for tickets in category_items.values():

                for ticket in tickets:

                    filename = str(ticket) + "." + category_name
                    to_remove.append(os.path.join(section_dir, filename))

    click.echo("I want to remove the following files:")

    for filename in to_remove:
        click.echo(filename)

    if not yes:
        # Not yet confirmed.
        yes = click.confirm('Is it okay if I remove those files?')

    if yes:
        call(["git", "rm", "--quiet"] + to_remove)


def stage_newsfile(directory, filename):

    call(["git", "add", os.path.join(directory, filename)])
