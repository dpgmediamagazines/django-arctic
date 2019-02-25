$(function() {
    /********** Change absolute uri for getting overview data as file ************/
    $('#csv_file_export').on('click', function () {
        var url = new URL(this.getAttribute('href'));
        url.searchParams.set('format', 'csv');
        this.setAttribute('href', url.href);
    })
});