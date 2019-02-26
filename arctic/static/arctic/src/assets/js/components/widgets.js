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

function datetimeformatter(django_date, format) {
    var date_valid = moment(django_date, format).isValid();
    if (!date_valid) {
        return null;
    } else {
        return moment(django_date, format).toDate();
    }
}

datetime_picker_settings.dateFormat = django2datepicker(datetime_picker_settings.dateFormat);
datetime_picker_settings.timeFormat = django2datepicker(datetime_picker_settings.timeFormat);
$.fn.datepicker.language['en'] = datetime_picker_settings;


function startSelectize() {
    $('[js-selectize]').each(function(index) {
        var instance = this;
        $(instance).selectize({
            allowEmptyOption: true,
            highlight: false,
            plugins: ['remove_button'],
            onFocus: function() {
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
                }
            }
        });
    });
}

function startSelectizeMultiple() {
    $('[js-selectize-multiple]').each(function(index) {
        var instance = this;
        $(instance).selectize({
            delimiter: ',',
            persist: false,
            plugins: ['remove_button'],
            onFocus: function() {
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
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
}

function startSelectizeAutocomplete() {
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
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
                }
            },
        });
    });
}

function startDatepicker() {
    $('[js-datepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-date"), $(this).attr('format') ? $(this).attr('format') : datetime_picker_settings.dateFormat);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            todayButton: true,
            language: 'en',
            startDate: date,
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
}

function startTimePicker() {
    $('[js-timepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-date"), $(this).attr('format') ? $(this).attr('format') : datetime_picker_settings.timeFormat);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            onlyTimepicker: true,
            language: 'en',
            startDate: date,
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
}

function startDateTimePicker() {
    $('[js-datetimepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-datetime"),  $(this).attr('format') ? $(this).attr('format') : `${datetime_picker_settings.dateFormat} ${datetime_picker_settings.timeFormat}`);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            language: 'en',
            todayButton: true,
            startDate: date,
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
}

function startListSorting() {
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

    $('[data-sorting-url] tr').on('dragstart', function(e) {
        $(this).css('opacity', '0.5');
        return true;
    });

    $('[data-sorting-url] tr').on('dragend', function(e) {
        $(this).css('opacity', 'inherit');
        return true;
    });
}

function startDynamicInlines() {
    let inlineFormSelector = '[data-inline-form]';
    $('[data-inline-button]').off().on('click', function(e){
        e.preventDefault();
        let $parent = $(this).parent();
        let $inlineForm = $parent.find(inlineFormSelector);
        inlineForm = $inlineForm[$inlineForm.length -1];
        selectizes = checkSelectizes();
        let $clonedInline = $(inlineForm).clone().removeClass('hide');
        $(inlineForm).before($clonedInline);
        if (selectizes) {
            startAllSelectizes();
        }
        startAllPickers();
    });

    function checkSelectizes() {
        $selectize = $(inlineForm).find('[js-selectize-multiple], [js-selectize-autocomplete], [js-selectize]');
        if ($selectize.length) {
            for(let i=0, len = $selectize.length; i < len; i++) {
                let selectize = $selectize[i];
                if (selectize.selectize) {
                    let value = $(selectize).val();
                    selectize.selectize.destroy();
                    $(selectize).val(value);
                }
            }
            return true
        }
        return false
    }
 }

 function startSortInlines() {
     $('[js-sort-inlines]').each(function(index) {
         Sortable.create(this, {
             onUpdate: function (e) {
                 let el = e.item.parentElement;
                 let orderFields = el.querySelectorAll('input[name*="-order"]');
                 if (orderFields.length) {
                     for(let i=0, len = orderFields.length; i < len; i++) {
                         field = orderFields[i];
                         field.value = i;

                         // Not needed if order fields are hidden
                         field.dispatchEvent(new Event('change'));
                     }
                 }
             }
         });
     });
 }


function startAll() {
    startAllSelectizes();
    startAllPickers();
    startListSorting();
}

function startAllSelectizes() {
    startSelectize();
    startSelectizeMultiple();
    startSelectizeAutocomplete();
}

function startAllPickers() {
    startDatepicker();
    startTimePicker();
    startDateTimePicker();
}


$(document).ready(function() {
    startAll();
    // tooltips
    $('[data-toggle="tooltip"]').tooltip()


    // dynamic inlines...
    startDynamicInlines();
    startSortInlines();
});
