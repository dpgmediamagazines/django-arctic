// convert date format specification from the django/php syntax to the js
// datepicker spec
function django2datepicker(django_format) {
    var translation_dict = {
        '%': '',
        'y': 'yy',
        'Y': 'yyyy',
        'm': 'mm',
        'd': 'dd',
        'H': 'hh',
        'I': 'hh',
        'M': 'ii',
        'p': 'aa',
        'S': ''
    }

    var datepicker_format = '';
    for (var i = 0, len = django_format.length; i < len; i++) {
        if (django_format[i] in translation_dict) {
            datepicker_format += translation_dict[django_format[i]];
        }
        else {
            datepicker_format += django_format[i];
        }
    }

    if (datepicker_format.slice(-1) == ':') {
        datepicker_format = datepicker_format.slice(0, -1);
    }
    return datepicker_format;
}


$(document).ready(function() {
    $('[js-selectize]').each(function(index) {
        $(this).selectize({
            allowEmptyOption: true,
            highlight: false,
            plugins: ['remove_button']
        });
    });

    $('[js-selectize-multiple]').each(function(index) {
        $(this).selectize({
            delimiter: ',',
            persist: false,
            plugins: ['remove_button'],
            onDropdownOpen: function($dropdown) {
                if ( $('form').hasClass('float-label') ) {
                    $dropdown.parent().next('label').css({
                        top: '.3rem',
                        fontSize: '75%'
                    });
                }
            },
            onDropdownClose: function($dropdown) {
                if ( $('form').hasClass('float-label') ) {
                    if ( $('.float-label .selectize-input').find('.item').length == 0 ) {
                        $dropdown.parent().next('label').css({
                            top: '.75rem',
                            fontSize: '100%'
                        });
                    }
                }
            },
            create: function(input) {
                return {
                    value: input,
                    text: input
                }
            }
        });
    });

    $('[js-selectize-autocomplete]').each(function(index) {
        var url = $(this).attr('data-url');
        $(this).selectize({
            valueField: 'value',
            labelField: 'label',
            searchField: 'label',
            create: false,
            load: function(query, callback) {
                if (!query.length) return callback();
                $.ajax({
                    url: url + encodeURIComponent(query),
                    type: 'GET',
                    error: function() {
                        callback();
                    },
                    success: function(res) {
                        callback(res.options);
                    }
                });
            },
            onDropdownOpen: function($dropdown) {
                $dropdown.parent().next('label').css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onDropdownClose: function($dropdown) {
                if ( $('.float-label .selectize-input').find('.item').length == 0 ) {
                    $dropdown.parent().next('label').css({
                        top: '.75rem',
                        fontSize: '100%'
                    });
                }
            },
        });
    });

    $('[js-datepicker]').each(function(index) {
        var date = new Date($(this).attr("data-date")) == 'Invalid Date' ? new Date() : new Date($(this).attr("data-date"))
        $(this).datepicker({
            todayButton: true,
            language: 'en',
            startDate: date,
            dateFormat: django2datepicker(DATE_FORMAT)
        });
    });

    $('[js-timepicker]').each(function(index) {
        var date = new Date($(this).attr("data-time")) == 'Invalid Date' ? new Date() : new Date($(this).attr("data-time"))
        $(this).datepicker({
            onlyTimepicker: true,
            language: 'en',
            startDate: date,
            timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true
        });
    });

    $('[js-datetimepicker]').each(function(index) {
        var date = new Date($(this).attr("data-datetime")) == 'Invalid Date' ? new Date() : new Date($(this).attr("data-datetime"))
        $(this).datepicker({
            language: 'en',
            todayButton: true,
            startDate: date,
            dateFormat: django2datepicker(DATE_FORMAT),
            timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true
        });
    });
});
