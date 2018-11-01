# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

Always reference the ticket number at the end of the issue description.


## [unreleased]

### Added
- blackened code
- added black check into CI
- Image file input now creates 2 events one on file selecting and another on removing

### Fixed
- field_label: changed 'optional' suffix rendering condition for disabled=False [#310][310]
- Image field: Removing and adding the same image on file inputs now works
- allowed to specify url with obj id for all action buttons [#318][318]

[310]: //github.com/sanoma/django-arctic/issues/310
[318]: //github.com/sanoma/django-arctic/issues/318


## 1.3.3.1

### Changed
- Changed slugify function, allow dashes (matches Django slugify)
- Added a few more characters with accents


## 1.3.3

### Changed
- Changed slugify function

### Breaking
- Previous slugify ignored characters with accents (é á etc...)
  This can affect existing slug depending on how the project is setup


## 1.3.3

- fix bug with iframe view containing params
- add variable in_modal to context
- listview: fix for getting reverse exception for links
  to related objects that are None.
- listview: make it compatible to annotate (group by)


## 1.3.2 (2018-07-24)

### Fixed

- get_actions: formaction dictionary was updated directly as class attribute
- get_actions: update dict in correct order


## 1.3.1 (2018-07-03)

### Added

- added documentation for authentication/roles

### Fixed

- fixed bug with required attribute in checkboxes and radio buttons
- improved logo display in the login screen
- fixed display of inline fields in forms without layouts


## 1.3.0 (2018-06-26)

### Added

- added a better default file/image upload widget [#173][173]

### Changed

- upgraded django-extra-views to 1.11 [#300][300]

## Fixed

- Calendar now displays the correct weekday labels


[173]: //github.com/sanoma/django-arctic/issues/173
[300]: //github.com/sanoma/django-arctic/issues/300


## 1.2.0 (2018-06-08)

### Added

- added data attribute data-id in base_data_table row to easily distinct rows [#296][296]
- added collapsible and collapsible_gettext helper functions to help define
  form layouts.
- added confirmation dialog support in Form actions [#294][294]
- added modal iFrame support in Lists (`tool_links`, `field_links`,
  `action_links`) and Forms (`actions`) [#243][243]
- extended tutorial documentation of Forms.

## Changed

- changed format of list items, simplified and moved to dict-like structure

[296]: //github.com/sanoma/django-arctic/issues/296
[294]: //github.com/sanoma/django-arctic/issues/294
[243]: //github.com/sanoma/django-arctic/issues/243


## 1.1.1 (2018-05-17)

### Changed

- in Forms, `help_text` is now displayed as a popup.

## Fixed

- SimpleSearchForm now works as expected, it can be replaced by a custom form
  with a variable number of fields

## Removed

- QuickFiltersFormMixin this is no longer needed, the same functionality can be
  added by using a `ChoiceField` with a `QuickFiltersSelect` or a
  `QuickFiltersSelectMultiple` widget.


## 1.1.0 (2018-04-20)

### Added

- Auto detect confirmation dialogs in ListViews - [#284][284]

### Changed

- `confirm_links` property in ListView changed to `modal_links` - [#284][284]
- deprecated `links` and replaced it with `actions` - [#287][287]
- expanded `tool_links` functionality - [#286][286]
- improved look and feel of the datetime picker and added localization to it
- added dutch localization

[284]: //github.com/sanoma/django-arctic/issues/284
[287]: //github.com/sanoma/django-arctic/issues/287
[286]: //github.com/sanoma/django-arctic/issues/286


## 1.0.2 (2018-03-19)

### Fixed

- Search bar items now join like a grouped button - [#267][267]
- Broken inline forms are working again - [#279][279]

## Changed

- added pagination_legend block and show_legend pagination option - [#277][277]
- added virtual_ordering_fields for ListView - [#274][274]
- added single and multiple select for quick filter - [#282][282]

[267]: //github.com/sanoma/django-arctic/issues/267
[277]: //github.com/sanoma/django-arctic/issues/277
[274]: //github.com/sanoma/django-arctic/issues/274
[279]: //github.com/sanoma/django-arctic/issues/279
[282]: //github.com/sanoma/django-arctic/issues/282


## 1.0.1 (2018-03-01)

### Fixed
- Search form JS submitting selector - [#248][248]
- Float Label styling for a number of HTML5 inputs - [#247][247]
- confirm_links feature in ListViews now works properly - [#54][54].
- Fixed displaying success message after DeleteView - [#270][270]

## Changed

- Folding side menu, menu settings - [#257][257]
- Improved pagination styles - [#265][265]

## Added

- Specifying `action_links` per each row in `ListView` - [#259][259]
- Specifying `field_classes` per each row in `ListView` - [#261][261]
- Specifying `QuickFiltersSelect` for filters_block in `ListView` - [#273][261]

[248]: //github.com/sanoma/django-arctic/issues/248
[247]: //github.com/sanoma/django-arctic/issues/247
[54]: //github.com/sanoma/django-arctic/issues/54
[257]: //github.com/sanoma/django-arctic/issues/257
[265]: //github.com/sanoma/django-arctic/issues/265
[259]: //github.com/sanoma/django-arctic/issues/259
[261]: //github.com/sanoma/django-arctic/issues/261
[265]: //github.com/sanoma/django-arctic/issues/265
[270]: //github.com/sanoma/django-arctic/issues/270
[269]: //github.com/sanoma/django-arctic/issues/269


## 1.0.0 (2018-01-31)

### Fixed

- Search forms and related widgets - [#242][242]

## Changed

- Updated Bootstrap to version 4.0.0
- Renamed `_search_form` `ListView` attrs, dropped compatibility with previous naming.

[242]: //github.com/sanoma/django-arctic/issues/242


## 1.0.0-beta2 (2018-01-19)

## Added

- Django 2.0 compatibility

## Removed

- Django 1.8 support


## 1.0.0-beta1 (2017-10-02)

## Added

- `DataListView`, a `ListView` that uses APIs as source of data - [#172][172]
- Float Labels option for form displays - [#221][221]

## Changed

- Moved from Foundation 6 to Bootstrap 4 - [#184][184]
- Improved tables look and feel - [#216][216]

### Removed

- `django-filter` dependency - [#213][213]
- `django-widget-tweaks` dependency

[172]: //github.com/sanoma/django-arctic/issues/172
[184]: //github.com/sanoma/django-arctic/issues/184
[213]: //github.com/sanoma/django-arctic/issues/213
[216]: //github.com/sanoma/django-arctic/issues/216
[221]: //github.com/sanoma/django-arctic/issues/221


## 0.9.7 (2017-06-13)

### Fixed

- Action Links now support named urls with parameters - [#165][165]

[165]: //github.com/sanoma/django-arctic/issues/165


## 0.9.6 (2017-04-25)

### Changed

- Added support for read-only fields in update view - [#72][72]
- Added support for media assets in Views and default templates - [#195][195]
- Bumped django-filters to 1.0.1 and fixed breaking changes - [#171][171]

[72]: //github.com/sanoma/django-arctic/issues/72
[171]: //github.com/sanoma/django-arctic/issues/171
[195]: //github.com/sanoma/django-arctic/issues/195


## 0.9.5 (2017-03-16)

### Changed

- Added full Django 1.10 compatibility - [#164][164]
- Added submenu icons display option - [#178][178]
- Considerate improved performance; no query per has_permission call - [#182][182]
- Check that 'next' redirect in the login view only goes to own host - [#186][186]

[164]: //github.com/sanoma/django-arctic/issues/164
[178]: //github.com/sanoma/django-arctic/issues/178
[182]: //github.com/sanoma/django-arctic/issues/182
[186]: //github.com/sanoma/django-arctic/issues/186


## 0.9.4 (2017-02-23)

### Changed

- Simplified the frontend tooling, removing Bower and foundation-cli, setup is
  now based on npm and gulp - [#161][161]

### Fixed

- In the listview, don't generate NoReverseMatch exception if any value of
  the arguments is None.

[161]: //github.com/sanoma/django-arctic/issues/161


## 0.9.3 (2016-10-27)

### Changed

- `FormView`, `CreateView` and `UpdateView` added a `layout` property to
  easily customize positioning and width of form fields - [#75][75]
- Added support for virtual fields in `ListView` - [#73][73]
- Improved the date/time picker in Date/Time fields - [#78][78]

[73]: //github.com/sanoma/django-arctic/issues/73
[75]: //github.com/sanoma/django-arctic/issues/75
[78]: //github.com/sanoma/django-arctic/issues/78
