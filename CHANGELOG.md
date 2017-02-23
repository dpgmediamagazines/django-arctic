#Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) 
and this project adheres to [Semantic Versioning](http://semver.org/).

Always reference the ticket number at the end of the issue description.

##0.9.4

##Fixed

- introduced self.get_ordering_fields()
- In the listview, don't generate NoReverseMatch exception if any value of the arguments is None.

##0.9.3 (2016-10-27)

###Changed

- `FormView`, `CreateView` and `UpdateView` added a `layout` property to 
  easily customize positioning and width of form fields - [#75][75]
- Added support for virtual fields in `ListView` - [#73][73]
- Improved the date/time picker in Date/Time fields - [#78][78]

[73]: //github.com/sanoma/django-arctic/issues/73
[75]: //github.com/sanoma/django-arctic/issues/75
[78]: //github.com/sanoma/django-arctic/issues/78
