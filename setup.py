from setuptools import (find_packages, setup)


__VERSION__ = '0.9.7'


def read_md(f):
    try:
        from pypandoc import convert
        return convert(f, 'rst')
    except ImportError:
        return open(f, 'r').read()


try:
    REQUIREMENTS = open('requirements/base.txt').read()
except:
    REQUIREMENTS = None

setup(
    name='django-arctic',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    version=__VERSION__,
    long_description=read_md('README.md'),
    install_requires=REQUIREMENTS,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    url='https://github.com/sanoma/django-arctic',
    author='Sanoma Netherlands',
    author_email='opensource@sanoma.com',
    description="Django framework to create custom content management systems",
)
