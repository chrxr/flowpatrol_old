var gulp = require('gulp');
var sass = require('gulp-sass')

gulp.task('base', function () {
    gulp.src('./flowpatrolcore/static/flowpatrolcore/css/scss/base.scss')
        .pipe(sass())
        .pipe(gulp.dest('./flowpatrolcore/static/flowpatrolcore/css/'));
});

gulp.task('tablet', function () {
    gulp.src('./flowpatrolcore/static/flowpatrolcore/css/scss/tablet.scss')
        .pipe(sass())
        .pipe(gulp.dest('./flowpatrolcore/static/flowpatrolcore/css/'));
});

gulp.task('default', ['base', 'tablet']);