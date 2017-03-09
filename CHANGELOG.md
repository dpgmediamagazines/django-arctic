#Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

Always reference the ticket number at the end of the issue description.

##Unreleased

###Changed

- Added full Django 1.10 compatibility - [#164][164]
- Considerate improved performance; no query per has_permission call - [#182][182]

[164]: //github.com/sanoma/django-arctic/issues/164
[182]: //github.com/sanoma/django-arctic/issues/182


##0.9.4 (2017-02-23)

###Changed

- Simplified the frontend tooling, removing Bower and foundation-cli, setup is 
  now based on npm and gulp - [#161][161]

###Fixed

- In the listview, don't generate NoReverseMatch exception if any value of 
  the arguments is None.

[161]: //github.com/sanoma/django-arctic/issues/161


##0.9.3 (2016-10-27)

###Changed

- `FormView`, `CreateView` and `UpdateView` added a `layout` property to 
  easily customize positioning and width of form fields - [#75][75]
- Added support for virtual fields in `ListView` - [#73][73]
- Improved the date/time picker in Date/Time fields - [#78][78]

[73]: //github.com/sanoma/django-arctic/issues/73
[75]: //github.com/sanoma/django-arctic/issues/75
[78]: //github.com/sanoma/django-arctic/issues/78
