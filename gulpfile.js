var gulp = require('gulp');
var sass = require('gulp-sass')

gulp.task('sass', function () {
    gulp.src('./flowpatrolcore/static/flowpatrolcore/css/scss/base.scss')
        .pipe(sass())
        .pipe(gulp.dest('./flowpatrolcore/static/flowpatrolcore/css/'));
});

gulp.task('default', ['sass']);