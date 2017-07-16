//Mobile menu controlss
$('#menu-button').click(function (e) {
    $(this).toggleClass('is-active');
    $('.row-offcanvas').toggleClass('active');
    e.preventDefault();
});

//Turn on Tooltips
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.split(search).join(replacement);
}

function lowerCaseKeys(dict) {
    var key, keys = Object.keys(dict);
    var n = keys.length;
    var new_dict={}
    while (n--) {
        key = keys[n];
        new_dict[key.toLowerCase()] = dict[key];
    }
    return new_dict;
}

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

function set_input_widgets() {
    var s = $('.js-selectize');
    if ( s.length ) {
        s.selectize(
            {
                allowEmptyOption: true,
                highlight: false,
                plugins: ['remove_button']
            }
        );
    }


    var s_tags = $('.js-selectize-tags');
    if (s_tags.length) {
        s_tags.selectize({
            delimiter: ',',
            persist: false,
            plugins: ['remove_button'],
            create: function(input) {
                return {
                    value: input,
                    text: input
                }
            }
        });
    }

    $('.js-selectize-autocomplete').each(function(index) {
        var url = $(this).attr('url');
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
            }
        });
    });

    $('.js-datepicker').each(function(index) {
        $(this).datepicker({
            todayButton: true,
            language: 'en',
            startDate: $(this).attr("date") == '' ? new Date() : new Date($(this).attr("date")),
        	dateFormat: django2datepicker(DATE_FORMAT)
        });
    });

    $('.js-timepicker').each(function(index) {
        $(this).datepicker({
            onlyTimepicker: true,
            language: 'en',
            startDate: $(this).attr("date") == '' ? new Date() : new Date($(this).attr("date")),
        	timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true
        });
    });

    $('.js-datetimepicker').each(function(index) {
        $(this).datepicker({
            language: 'en',
            todayButton: true,
            startDate: $(this).attr("date") == '' ? new Date() : new Date($(this).attr("date")),
        	dateFormat: django2datepicker(DATE_FORMAT),
            timeFormat: django2datepicker(TIME_FORMAT),
            timepicker: true
        });
    });
}

// jquery stuff goes here
$(document).ready(function() {
    // Stepper input
    var $stepperInput = $('.stepper-input input');

    function incrementStepperInput(amount) {
        $stepperInput.val((parseInt($stepperInput.val()) || 0) + amount);
    }

    var stepperInputDecrement = $('.stepper-input button')[0];
    $(stepperInputDecrement).click(function() {
        incrementStepperInput(-1);
    });

    var stepperInputIncrement = $('.stepper-input button')[1];
    $(stepperInputIncrement).click(function() {
        incrementStepperInput(1);
    });

    var dirty_check = $('form.dirty-check');
    if (dirty_check.length && !window.parent != window ) {
        dirty_check.areYouSure();

        $('form').on('dirty.areYouSure', function() {
            var tab = $('.tabs-title.is-active a')[0];
            if (tab && (tab.text[0] != '●')) {
                tab.text = '● ' + tab.text;
            }
            document.title = '● ' + document.title;
        });

        $('form').on('clean.areYouSure', function() {
            var tab = $('.tabs-title.is-active a')[0];
            if (tab) {
                tab.text = tab.text.slice(2);
            }
            document.title = document.title.slice(2);
        });
    }

    set_input_widgets();
});
