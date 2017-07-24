'use strict';

import plugins  from 'gulp-load-plugins';
import yargs    from 'yargs';
import gulp     from 'gulp';
import rimraf   from 'rimraf';
import yaml     from 'js-yaml';
import fs       from 'fs';

// Load all Gulp plugins into one variable
const $ = plugins();

// Check for --production flag. Compresses everything, doesn't generate an
// source map etc so the final result is nice and clean for production usage
const PRODUCTION = !!(yargs.argv.production);

// Load settings from settings.yml
const { COMPATIBILITY, PORT, UNCSS_OPTIONS, PATHS } = loadConfig();

function loadConfig() {
    let ymlFile = fs.readFileSync('config.yml', 'utf8');
    return yaml.load(ymlFile);
}

// Build the "dist" folder by running all of the below tasks
gulp.task('build', gulp.series(clean, gulp.parallel(sass, javascript, images, copy, copyFonts)));

// Build the site for development purpose
gulp.task('default', gulp.series('build', watch));

// Delete the "dist" folder, this happens every time a build starts
function clean(done) {
    rimraf(PATHS.dist, done);
}

// Copy files out of the assets folder
// This task skips over the "img", "js", and "scss" folders, which are parsed separately
function copy() {
    return gulp.src(PATHS.assets)
    .pipe(gulp.dest(PATHS.dist + '/assets'));
}

// Copy files out the fonts from the fontawesome folder
function copyFonts() {
    return gulp.src('./node_modules/font-awesome/fonts/*')
    .pipe(gulp.dest(PATHS.dist + '/assets/fonts'));
};

// Compile Sass into CSS. In production, the CSS is compressed
function sass() {
    return gulp.src('src/assets/scss/arctic.scss')
    .pipe($.sourcemaps.init())
    .pipe($.sass({
        includePaths: PATHS.sass,
        outputStyle: 'compressed'
    })
    .on('error', $.sass.logError))
        .pipe($.autoprefixer({
        browsers: COMPATIBILITY
    }))

    // Comment in the pipe below to run UnCSS in production
    // .pipe($.if(PRODUCTION, $.uncss(UNCSS_OPTIONS)))
    .pipe($.if(PRODUCTION, $.cssnano()))
    .pipe($.if(!PRODUCTION, $.sourcemaps.write()))
    .pipe(gulp.dest(PATHS.dist + '/assets/css'))
}

// Combine JavaScript into one file. In production, the file is minified
function javascript() {
  return gulp.src(PATHS.javascript)
    .pipe($.sourcemaps.init())
    .pipe($.babel())
    .pipe($.concat('app.js'))
    .pipe($.if(PRODUCTION, $.uglify()
      .on('error', e => { console.log(e); })
    ))
    .pipe($.if(!PRODUCTION, $.sourcemaps.write()))
    .pipe(gulp.dest(PATHS.dist + '/assets/js'));
}

// Copy images to the "dist" folder. In production, the images are compressed
function images() {
    return gulp.src('src/assets/img/**/*')
    .pipe($.if(PRODUCTION, $.imagemin({
        progressive: true
    })))
    .pipe(gulp.dest(PATHS.dist + '/assets/img'));
}

// Watch for changes to static assets, Sass, and JavaScript
function watch() {
    gulp.watch(PATHS.assets, copy);
    gulp.watch('src/assets/scss/**/*.scss', sass);
    gulp.watch('src/assets/js/**/*.js').on('change', gulp.series(javascript));
    gulp.watch('src/assets/img/**/*').on('change', gulp.series(images));
}
