$(function() {
    /********** Getting table data as file ************/
    $('#csv_file_import').on('click', function () {
        var table = $('table'),
            page_title = document.querySelector('.header__title'),
            actionColumns = document.querySelectorAll('td .list-actions'),
            fileName = page_title ? page_title.innerText: 'tabledata';
        if (actionColumns.length > 0){
            // hide action list column
            table.find('tr').find('td:eq(-1),th:eq(-1)').hide();
            saveTableToFile();
            table.find('tr').find('td:eq(-1),th:eq(-1)').show();
        } else{
            saveTableToFile();
        }

        function saveTableToFile() {
        table.table2csv({
            type: "csv",
            filename: fileName + '.csv',
        });
    }
    })
});