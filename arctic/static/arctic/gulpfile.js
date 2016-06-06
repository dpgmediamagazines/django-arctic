var gulp = require('gulp');
var config = require('./config.json');
const del = require('del');
var $    = require('gulp-load-plugins')();


// copy images into build
gulp.task('copy:images', function() {
  gulp.src([ config.path.src + config.path.images + '/**/*'])
    .pipe(gulp.dest( config.path.build + config.path.images ));
});

// copy javascript into build
gulp.task('copy:javascript', function() {
  gulp.src([ config.path.src + config.path.javascript + '/**/*'])
    .pipe(gulp.dest( config.path.build + config.path.javascript ));

});

// delete unnecessary files
gulp.task('cleanup', function() {
    del.sync([
        'build/components/font-awesome/less',
        'build/components/foundation/css',
        'build/components/jquery/src',
        'build/components/modernizr/feature-detects',
        'build/components/modernizr/media',
        'build/components/modernizr/test',
        'build/components/motion-ui/docs',
        'build/components/Snap.svg/doc',
    ]);
});


// bundle copy tasks
gulp.task('copy', ['copy:images', 'copy:javascript']);


// run sass
gulp.task('sass', function() {
  return gulp.src( config.path.src + config.path.scss + config.sass.main )
      .pipe( $.sass( {
              includePaths: config.sass.modules,
              outputStyle: config.sass.outputStyle,
          } )
          .on( 'error', $.sass.logError ) )
      .pipe( $.autoprefixer( {
          browsers: config.autoprefixer.browsers
      } ) )
      // Todo: add build date
      .pipe( gulp.dest( config.path.build + config.path.css ) );
});


// TODO: minify js files (but keep seperate)
gulp.task('default', ['copy', 'sass'], function() {
  gulp.watch([ config.path.src + config.path.scss + '**/*.scss'], ['sass']);
  gulp.watch([ config.path.src + config.path.images + '**/*.*'], ['copy:images']);
  gulp.watch([ config.path.src + config.path.javascript + '**/*.js'], ['copy:javascript']);
});

// build new assets
gulp.task('build', ['copy', 'sass', 'cleanup']);