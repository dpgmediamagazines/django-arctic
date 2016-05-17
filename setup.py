from setuptools import setup, find_packages


__VERSION__ = '0.1.0'

try:
    README = open('README.md').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = None

setup(
    name='django-arctic',
    version=__VERSION__,
    long_description=README,
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    license='MIT',
    url='https://source.sanoma.com/projects/REUSE/repos/arctic/browse',
    author='Sjoerd Arendsen',
    author_email='sjoerd.arendsen@sanoma.com',
    description="A CMS creation framework for Django",
)
