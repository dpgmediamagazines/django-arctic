#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import os
import stat
from optparse import OptionParser

from django.core.management import ManagementUtility


def create_project(parser, options, args):
    # Validate args
    if len(args) < 2:
        parser.error("Please specify a name for your Arctic installation")
    elif len(args) > 3:
        parser.error("Too many arguments")

    project_name = args[1]
    try:
        dest_dir = args[2]
    except IndexError:
        dest_dir = ""

    # Make sure given name is not already in use by another
    # python package/module.
    try:
        __import__(project_name)
    except ImportError:
        pass
    else:
        parser.error(
            '"{}" conflicts with the name of an existing '
            "Python module and cannot be used as a project "
            "name. Please try another name.".format(project_name)
        )

    print("Creating an Arctic project named {}".format(project_name))

    # Create the project from the Arctic template using startapp

    # First find the path to Arctic
    import arctic

    arctic_path = os.path.dirname(arctic.__file__)
    template_path = os.path.join(arctic_path, "project_template")

    # Call django-admin startproject
    utility_args = [
        "django-admin.py",
        "startproject",
        "--template=" + template_path,
        "--ext=html,rst",
        project_name,
    ]

    if dest_dir:
        utility_args.append(dest_dir)

    utility = ManagementUtility(utility_args)
    utility.execute()

    # add execute permission to manage.py, somehow it gets lost on the way
    manage_py = os.path.join(dest_dir or project_name, "manage.py")
    st = os.stat(manage_py)
    os.chmod(
        manage_py, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )

    print(
        "Congratulations! {0} has been created.\n"
        "The next steps are:\n"
        "- In config/settings.py change the database settings (if needed).\n"
        "- Run database migrations: {0}/manage.py migrate.\n"
        "- Create an admin user: {0}/manage.py createsuperuser.\n"
        "- Finally run the project: {0}/manage.py runserver.\n".format(
            project_name
        )
    )


COMMANDS = {"start": create_project}


def main():
    # Parse options
    parser = OptionParser(usage="Usage: arctic start project_name [directory]")
    (options, args) = parser.parse_args()

    # Find command
    try:
        command = args[0]
    except IndexError:
        parser.print_help()
        return

    if command in COMMANDS:
        COMMANDS[command](parser, options, args)
    else:
        parser.error("Unrecognised command: " + command)


if __name__ == "__main__":
    main()
