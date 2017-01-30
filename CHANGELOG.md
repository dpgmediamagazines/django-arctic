#Changelog

Arctic uses semantic versioning - please refer to <http://semver.org> for further details.

##0.9.4

- bugfix: get_field_value didn't use get_fields but self.fields
- introduced self.get_ordering_fields()
- introduced self.get_search_fields()
- introduced self.get_filter_fields()

##0.9.3 (2016-10-27)

###Changes

- `FormView`, `CreateView` and `UpdateView` added a `layout` property to 
  easily customize positioning and width of form fields - [#75][75]
- Added support for virtual fields in `ListView` - [#73][73]
- Improved the date/time picker in Date/Time fields - [#78][78]

[73]: //github.com/sanoma/django-arctic/issues/73
[75]: //github.com/sanoma/django-arctic/issues/75
[78]: //github.com/sanoma/django-arctic/issues/78
