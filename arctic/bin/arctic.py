#!/usr/bin/env python
from __future__ import absolute_import, print_function, unicode_literals

import os
import stat
from optparse import OptionParser

from django.core.management import ManagementUtility


class bcolors:
    """
    ANSI escape sequences for terminal colors
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
    template_path = os.path.join(arctic_path, "project_template/start")

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


def create_app(parser, options, args):
    # Validate args
    if len(args) < 2:
        parser.error("Please specify a name for your app")
    elif len(args) > 3:
        parser.error("Too many arguments")

    app_name = args[1].lower()

    try:
        dest_dir = args[2]
    except IndexError:
        dest_dir = ""

    # Make sure given name is not already in use by another
    # python package/module.
    try:
        __import__(app_name)
    except ImportError:
        pass
    else:
        parser.error(
            '"{}" conflicts with the name of an existing '
            "Python module and cannot be used as an app "
            "name. Please try another name.".format(app_name)
        )

    print(
        (
            bcolors.HEADER + "Creating an App named {}" + bcolors.ENDC + "\n"
        ).format(app_name)
    )

    # First find the path to Arctic
    import arctic

    arctic_path = os.path.dirname(arctic.__file__)
    template_path = os.path.join(arctic_path, "project_template/app")

    # Call django-admin starrtapp
    utility_args = [
        "django-admin.py",
        "startapp",
        "--template=" + template_path,
        app_name,
    ]

    if dest_dir:
        utility_args.append(dest_dir)

    utility = ManagementUtility(utility_args)
    utility.execute()

    print(
        (
            "Congratulations! {0} folder has been created it contains the "
            "following structure.\n\n" + bcolors.OKBLUE + " -{0}\n"
            " ---__init__.py\n"
            " ---apps.py\n"
            " ---forms.py\n"
            " ---models.py\n"
            " ---urls.py\n"
            " ---views.py\n\n" + bcolors.ENDC + "The next steps are:\n\n"
            "  Add the app name to "
            + bcolors.UNDERLINE
            + "INSTALLED_APPS"
            + bcolors.ENDC
            + " in the settings.py\n"  # NOQA
            + bcolors.OKGREEN
            + '"{0}",'
            + bcolors.ENDC
            + "\n"
            "  Add the app name and path to "
            + bcolors.UNDERLINE
            + "ARCTIC_MENU"
            + bcolors.ENDC
            + " in the settings.py\n"  # NOQA
            + bcolors.OKGREEN
            + '("{1}", "{0}:list", "fa-folder"),'
            + bcolors.ENDC
            + "\n"  # NOQA
            "  Add the urls to config/urls.py.\n"
            + bcolors.OKGREEN
            + 'url(r"^{0}/", include("{0}.urls", "{0}")),'
            + bcolors.ENDC
            + "\n"  # NOQA
            "  Add fields in the models.py file\n"
            "- Run "
            + bcolors.OKGREEN
            + "./manage.py makemigrations {0}"
            + bcolors.ENDC
            + "\n"  # NOQA
            "- Run "
            + bcolors.OKGREEN
            + "./manage.py migrate"
            + bcolors.ENDC
            + "\n\n"  # NOQA
            "The "
            + bcolors.BOLD
            + "forms.py"
            + bcolors.ENDC
            + " has a form with all the fields in the model and \n"  # NOQA
            "the "
            + bcolors.BOLD
            + "views.py"
            + bcolors.ENDC
            + " contains views for list, create, edit and delete. \n"  # NOQA
            "All of then can be tweaked to better satisfy the needs of the "
            "project/app\n"
        ).format(app_name, app_name.capitalize())
    )


COMMANDS = {
    "start": create_project,
    "createapp": create_app,
}


def main():
    # Parse options
    parser = OptionParser(
        usage="Usage: arctic start project_name [directory]"
        "Usage: arctic createapp appname [directory]"
    )
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
