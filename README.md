#Django Arctic

Django Arctic is a framework that simplifies the creation of custom content management systems.

## Quickstart

Clone or download the arctic repository,

Create a virtualenv:

	mkvirtualenv arctic

or with pyenv:

    pyenv virtualenv 2.7.11 arctic
    pyenv local arctic

Install requirements

	pip install -r demo/requirements.txt


Run migrate

	python manage.py migrate


Start runserver

	python manage.py runserver


Profit!

## TODO

- Create Permission layer, make class based
- Rewrite menu system, make class based
- Rewrite filter system. Make class based
- Subclass extra_views views into our own views. So we can alter where needed in the future.
- Create default dashboard settings file. (DASHBOARD_SITE_NAME, DASHBOARD_LOGO etc)
- Make frontend stuff sweet and reusable. Its just a out of the box bootstrap theme right now (need frontender for this)
- Rewrite django template lookup to include our base CRUD templates (detail, list, delete, create)
- Make better filtering template tags for frontend usage. Like sorting and ordering url builder.
- Add templatetags to build list_display_links in templates


## Discussion points

- The name: Django Artic?
- If we are going for a framework. Whe should make the frontend dashboard an optional component?
- Maybe MAYBE think of viewsets when everything is class based.
- Frontend
-- static within repo or build it on spot to get the latest and greatest.

## Frontend

Arctic base theme has been build with Zurb Foundation for sites, documentation of the Foundation framework is available at http://foundation.zurb.com/sites/docs/

### Notices:
- NodeJS is required to develop in frontend code
- Frontend dependecies should be installed with bower

#### Workflow:
 - Develop in src folder
 - Gulp watch and build task updates build folder
 - Changed in build folder needs to be commited into he repo

#### SCSS:

 - The default grid with floats is disabled, the flexbox version is enabled since this gives easier and more powerfull aligment options etc. Make sure the default grid system keeps disabled since it uses the same variables as the flex grid system and they don't work nice together.
 - Inside the scss folder there are 2 setting files, the _settings.scss file contains the default variables of the Foundation framework. To make sure settings aren't overwritten when updating the Foundation framework an _project-settings.scss file is created. Default values can be overwritten here. To keep things simple and prevent cluttering the base variables like margins, fonts etc are defined here also.
 - There are multiple folders inside the scss base folder named modules, pages, partials and vendor. Explanation for each folder below

 `Modules: Contain everything that doesn't ouput css by itself. Mixins, functions etc can be placed here`

 `Partials: Basic and global styling can be placed inside this folder.`

 `Pages: Page specific overrides can be placed here, overides should be based on the body class to prevent large class arrays`

### Development installation:

Development installation is pretty straight forward, make sure npm (nodejs) is installed (don't run it as root) and following commands should get everything up and running.

 1. if not already installed, install nodejs: https://nodejs.org/en/
 2. cd into `cd arctic/static/arctic`
 3. run `npm i` (don't run it as root)
 4. run `gulp` (starts the default gulp task that is a watcher and compiles scss to css)

### Frontend deployment

If the frontend needs to be build on deploy (for in example with Bamboo), fire the following commands subscribed below 'development installation' and add the following command.

 5. npm run clean:tools (Removes node modules that were required to build static's)

### Troubleshooting:
Most of the times when this happens, there's a corrupt node module.

 1. cd into `cd arctic/static/arctic`
 2. run `npm run clean` (this removes all develop dependecies and compiled files)
 3. run `npm i` (fresh install of develop dependecies and new compiled files)

If the problem stil occurs check error log: /arctic/static/arctic/npm-debug.log

### Something to think about:
Don't install anything that isn't absolutely necessary with NPM or Bower. Foundation gives an good base with more than enough options. If additional components are installed make sure there is documentation and it doesn't break anywthing when somebody is doing an fresh install.

### Docs:
Foundation docs: http://foundation.zurb.com/sites/docs/ (base framework)
Motion UI docs: https://github.com/zurb/motion-ui/blob/master/docs/animations.md (Foundation animation library)
Abide: http://foundation.zurb.com/sites/docs/abide.html (Used for form validation, default foundation library)