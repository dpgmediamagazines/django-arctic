$(document).foundation();

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

function inlineWidget(css_class, template, dict, list_separator) {
    $('.inline-widget.' + css_class).html(function(i, content) {
        var has_link = false;
        var text = $(content).text();
        var result = "";
        if ($(content).attr('href')) {
            text = $(content).children(':first').text();
            has_link = true;
        }

        var text_list = [text];
        if (list_separator) {
            text_list = text.split(list_separator);
        }

        for (i = 0; i < text_list.length; i++)
        {
            var item = text_list[i];
            if (list_separator) {
                item += list_separator;
            }

            if (!dict) {
                item = template.replaceAll('{{ key }}', text_list[i]);
            }
            else {
                var lower_dict = lowerCaseKeys(dict);
                var lower_text_item = text_list[i].toLowerCase();

                if (lower_text_item in lower_dict) {
                    item = template.replaceAll('{{ value }}', lower_dict[lower_text_item]);
                    item = item.replaceAll('{{ key }}', text_list[i]);
                }
            }
            result += item;
        }

        if (has_link) {
            result = $(content).empty().append(result);
        }

        return result;
    });
}

function set_input_widgets() {
    var s = $('.js-selectize');
    if ( s.size() ) {
        s.selectize(
            {
                allowEmptyOption: true,
                highlight: false,
                plugins: ['remove_button']
            }
        );
    }


    var s_tags = $('.js-selectize-tags');
    if (s_tags.size()) {
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

    // Toggle menu burger to cross
    var canvas = $( '.off-canvas' );
    var hamburger = $('#menu-button');

    canvas.on('opened.zf.offcanvas', function () {
        hamburger.addClass('is-active');
    });

    canvas.on('closed.zf.offcanvas', function () {
        hamburger.removeClass('is-active');
    });

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
    if (dirty_check.size() && !window.parent != window ) {
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