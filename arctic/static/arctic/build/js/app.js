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
            item = text_list[i];
            if (list_separator) {
                item += list_separator;
            }

            if (!dict) {
                item = template.replaceAll('{{ key }}', text_list[i]);
            }
            else {
                lower_dict = lowerCaseKeys(dict);
                lower_text_item = text_list[i].toLowerCase();

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

// jquery stuff goes here
$(document).ready(function() {

    // Toggle menu hamburger to cross
    $('#menu-button').click(function (e) {
        $('#menu-button').toggleClass('is-active');
        // e.preventDefault();
    });

    // Toggle back menu button into hamburger when clicking overlay
    $('.js-off-canvas-exit').click(function(e) {
        $('#menu-button').removeClass('is-active');
        // e.preventDefault();
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

    $('.chosen-select').chosen({width: '100%', disable_search_threshold: 10});

    $('form.dirty-check').areYouSure();

    $('form').on('dirty.areYouSure', function() {
        var tab = $('.tabs-title.is-active a')[0];
        if (tab) {
            tab.text = '●' + tab.text;
        }
        document.title = '●' + document.title;
    });

    $('form').on('clean.areYouSure', function() {
        var tab = $('.tabs-title.is-active a')[0];
        if (tab) {
            tab.text = tab.text.slice(1);
        }
        document.title = document.title.slice(1);
    });

});

