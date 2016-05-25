$(document).foundation();

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

    function listWidget(css_class, template, dict) {
        $('.list-widget.' + css_class).html(function(i, content) {
            var has_link = false;
            var text = $(content).text();
            var result = content;
            if ($(content).attr('href')) {
                text = $(content).children(':first').text();
                has_link = true;
            }
            if (text in dict) {
                result = template.replace('{{ value }}', dict[text]);
                result = result.replace('{{ key }}', text);
                if (has_link) {
                    result = $(content).empty().append(result)
                }
            }
            return result;
        });
    }

    var template = '<i title="{{ key }}" style="color:{{ value }}" class="fa fa-circle"></i>';
    var dict = {"False": "red", "True": "green"};
    listWidget('boolean-circle', template, dict);

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

    $('.chosen-select').chosen({width: '95%'});
});

