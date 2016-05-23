$(document).foundation();

// jquery stuff goes here
$(document).ready(function() {

    // Toggle menu hamburger to cross
    $('#menu-button').click(function (e) {
        $('#menu-button').toggleClass('is-active');
        e.preventDefault();
    });

    // Toggle back menu button into hamburger when clicking overlay
    $('.js-off-canvas-exit').click(function(e) {
        $('#menu-button').removeClass('is-active');
        e.preventDefault();
    });


    // Stepper input
    var $stepperInput = $('.stepper-input input');

    function incrementStepperInput(amount) {
        $stepperInput.val((parseInt( $stepperInput.val()) || 0) + amount);
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

