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

### Custom Events
* Events
    * Event name:  ```arcticImageAdded```
        * Event data: ```input html element```
        * Occurs after selecting an image on an Image field (similar to the JS change event on a file input)
    * Event name:  ```arcticImageRemoved```
        * Event data: ```input html element```
        * Occurs after removing an image from a Image field

    #
    Events can be listened with
    ```
    document.addEventListener('eventname', function (e) {
        //code to execute
        //access the data with
        console.log(e.detail)
    }, false);
    ```

### Javascript widgets (all of them are initialised on DOM load event)
`startSelectize()` - Starts simple selectize
`startSelectizeMultiple()` - Starts multiple selectize
`startSelectizeAutocomplete()` - Starts autocomplete selectize
`startAllSelectizes()` - Starts all 3 selectizes
`startDatepicker()` - Starts datepicker
`startTimePicker()` - Starts timepicker
`startDateTimePicker()` - Starts date and time picker
`startAllPickers()` - Starts all 3 pickers
`betterFile()` - Starts better file input for image fields
`startAllWidgets()` - Starts all of the above

### Show/Hide loading icon
`show_artic_loader()` - Shows a loading icon (if none is already there) in the center of the screen
`hide_artic_loader()` - Hides loading icon
