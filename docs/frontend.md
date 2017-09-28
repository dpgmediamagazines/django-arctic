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
