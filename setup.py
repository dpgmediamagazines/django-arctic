import os
import shutil
import sys
from setuptools import find_packages, setup

__VERSION__ = "1.4.0"


def read_md(f):
    try:
        from pypandoc import convert

        return convert(f, "rst")
    except ImportError:
        return open(f, "r").read()


def check_installed(*packages):
    exit = False
    # if not a list, let's make it into one
    for package in packages:
        if os.system("pip freeze | grep {} >/dev/null".format(package)):
            print("{0} not installed: use `pip install {0}`".format(package))
            exit = True
    if exit:
        print("Exiting.")
        sys.exit()


def check_tagged_version(version):
    current_branch_is_master = not os.system(
        "git rev-parse --abbrev-ref HEAD | grep master >/dev/null"
    )
    master_is_tagged = not os.system(
        "git tag --points-at master | grep {} >/dev/null".format(version)
    )
    if not current_branch_is_master:
        print("Publish can only be done from the master branch.")
    if not master_is_tagged:
        print(
            "`{}` tag has not been created on the master branch.".format(
                version
            )
        )
    if not (current_branch_is_master and master_is_tagged):
        print("Exiting.")
        sys.exit()


try:
    REQUIREMENTS = open("requirements/base.txt").read()
except Exception:
    REQUIREMENTS = None

if sys.argv[-1] == "publish":
    check_installed("pypandoc", "twine")
    check_tagged_version(__VERSION__)
    os.system("python setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")
    shutil.rmtree("build")
    shutil.rmtree("dist")
    sys.exit()


setup(
    name="django-arctic",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    version=__VERSION__,
    long_description=read_md("README.md"),
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    entry_points={"console_scripts": ["arctic = arctic.bin.arctic:main"]},
    license="MIT",
    url="https://github.com/sanoma/django-arctic",
    author="Sanoma Netherlands",
    author_email="opensource@sanoma.com",
    description="Django framework to create custom content management systems",
)
