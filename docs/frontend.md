# Frontend

The Arctic User Interface is based on
[Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
and includes extra UI elements such as a responsive sidebar, float label fields
and customizable colors with CSS properties.

The Arctic build already includes precompiled frontend assets, so the frontend
tooling mentioned in this document is only needed if you want to do frontend
development for the Django Arctic project or need to create a custom UI based
on a copy of the Arctic setup and bypass the default setup on your own project.


## Requirements

- [npm](https://www.npmjs.com) to manage dependencies
- [gulp](https://gulpjs.com) for automation

## Setup

In the terminal:

- In the Arctic project go to `arctic/static/arctic`
- Install all dependencies: `npm install`
- Set gulp to watch all file changes `gulp`


## File structure

All development should be done in the `src` folder, do not edit files in `dist`
or add any dependencies by hand in `node_modules`!

### Before creating a pull request
Because the project contains all the compiled files, if there are any changes
to the css or js the command `gulp build --production` should be run before
the last commit, this will guarantee that the arctic.css and arctic.js are minified

### Non Bootstrap libraries
- [Datepicker](https://github.com/t1m0n/air-datepicker)
- [Selectize](https://selectize.github.io/selectize.js/)
- [Sortable](https://github.com/RubaXa/Sortable)

Datapicker and Selectize are initialed in the `widgets.js` file

Sortable obeys the following rules:
```
Required html data attributes:
* data-sortable - initiates sortable)
* data-row - defines a row to sort

Optional
* data-sort-handle - to specify a specific dragging handle
* data-sort-placeholder - field to save position of row

* data-delete-handle - delete button
* data-delete-placeholder - field to check as delete
```
