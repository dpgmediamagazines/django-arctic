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
        var instance = this;
        $(instance).selectize({
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
                    if (!$(instance).find('.has-items')) {
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
        var instance = this
        var url = $(instance).attr('data-url');
        $(instance).selectize({
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
            onFocus: function() {
                //alert($(instance).next('label'));
                $(instance).next('label').css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ( $(instance).find('.item').length == 0 ) {
                    $(instance).next('label').css({
                        top: '.75rem',
                        fontSize: '100%'
                    });
                }
            },
        });
    });

    $('[js-datepicker]').each(function(index) {
        var date = new Date($(this).attr("data-date")) == 'Invalid Date' ? null : new Date($(this).attr("data-date"))
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            todayButton: true,
            language: 'en',
            startDate: date,
            dateFormat: django2datepicker(DATE_FORMAT),
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })

        }).data('datepicker').selectDate(date);
    });

    $('[js-timepicker]').each(function(index) {
        var date = new Date($(this).attr("data-time")) == 'Invalid Date' ? null : new Date($(this).attr("data-time"))
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            onlyTimepicker: true,
            language: 'en',
            startDate: date,
            timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true,
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })
        }).data('datepicker').selectDate(date);
    });

    $('[js-datetimepicker]').each(function(index) {
        var date = new Date($(this).attr("data-datetime")) == 'Invalid Date' ? null : new Date($(this).attr("data-datetime"))
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            language: 'en',
            todayButton: true,
            startDate: date,
            dateFormat: django2datepicker(DATE_FORMAT),
            timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true,
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })
       }).data('datepicker').selectDate(date);
    });

    // sortable ListViews
    $('[data-sorting-url]').each(function(index) {
        var url = $(this).attr('data-sorting-url');
        var updated_items = new Object();
        Sortable.create(this, {
            handle: '.drag-handle',
            animation: 100,
            onUpdate: function (/**Event*/evt) {
                var base_sorting_value = 1;
                $(evt.to).find('.drag-handle i').each(function(index) {
                    var key = $(this).attr('data-sorting-key');
                    var value = $(this).attr('data-sorting-value');
                    if (parseInt(value) != base_sorting_value) {
                        updated_items[key] = base_sorting_value;
                        $(this).attr('data-sorting-value', base_sorting_value);
                    }
                    base_sorting_value += 1;
                });
                $.post(url, JSON.stringify(updated_items))
                .done(function() {
                    // keep this empty for now
                })
                .fail(function() {
                    console.error('Unable to post reordering to backend')
                })
            }
        });
    });
});
