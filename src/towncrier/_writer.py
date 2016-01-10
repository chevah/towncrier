# Copyright (c) Amber Brown, 2015
# See LICENSE for details.

"""
Responsible for writing the built news fragments to a news file without
affecting existing content.
"""

from __future__ import absolute_import, division

import os


TOWNCRIER_START = ".. towncrier release notes start\n"


def append_to_newsfile(directory, filename, name_and_version, content):

    news_file = os.path.join(directory, filename)

    if not os.path.exists(news_file):
        existing_content = ""
    else:
        with open(news_file, "r") as f:
            existing_content = f.read()

    top_line = name_and_version + "\n" + "-" * len(name_and_version) + "\n\n"

    latest_version = name_and_version.split(',', 1)[0]
    if latest_version in existing_content:
        raise ValueError(
            "It seems you've already produced newsfiles for this version?")

    # existing_content = existing_content.split(TOWNCRIER_START)
    last_version = existing_content.find('\n\nVersion ')
    existing_content = [
        existing_content[:last_version],
        existing_content[last_version:],
        ]

    with open(os.path.join(directory, filename), "w") as f:

        if len(existing_content) > 1:
            f.write(existing_content.pop(0) + '\n\n')

        f.write(top_line)
        f.write(content)
        if existing_content[0]:
            f.write("\n\n")
        f.write(existing_content[0].lstrip())
