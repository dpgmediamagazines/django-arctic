from setuptools import (find_packages, setup)


__VERSION__ = '0.9.4'

try:
    README = open('README.md').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements/base.txt').read()
    # setup.py does not accept link dependencies mixed with PyPI ones, so 
    # the django-extra-views package name and its github link are setup here 
    # and another reference is kept in requirements/test.txt. When a new version 
    # of django-extra-views is released this setup can be simplified.
   REQUIREMENTS += '\ndjango-extra-views==0.8.0'
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    version=__VERSION__,
    long_description=README,
    install_requires=REQUIREMENTS,
    dependency_links=['https://github.com/AndrewIngram/' +\
                      'django-extra-views/tarball/' +\
                      'dd5d6b877945eeca6ee04930a7fa441e66a586b0' +\
                      '#egg=django-extra-views-0.8.0'],
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    url='https://github.com/sanoma/django-arctic',
    author='Sanoma Netherlands',
    author_email='opensource@sanoma.com',
    description="Django framework to create custom content management systems",
)
