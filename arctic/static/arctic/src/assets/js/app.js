!(function(w, $) {
//Mobile menu controls
$('#menu-button').click(function (e) {
    $(this).toggleClass('is-active');
    $('.row-offcanvas').toggleClass('active');
    e.preventDefault();
});

let collapseButton = document.querySelectorAll('[js--collapse-menu]');

for (var i = 0; i < collapseButton.length; i++) {
    collapseButton[i].addEventListener('click', function(event) {
        event.preventDefault();
        if (this.getAttribute('data-stay-open')) {
            return false;
        }
        let el = this.querySelector('[js--collapse-menu-arrow]');

        this.classList.toggle('active');
        if (el.classList.contains('fa-angle-down')) {
            el.classList.remove('fa-angle-down');
            el.classList.add('fa-angle-left');
        } else {
            el.classList.add('fa-angle-down');
            el.classList.remove('fa-angle-left');
        }
        this.nextSibling.nextSibling.classList.toggle('active');
    });
}

})(window, $);
//Turn on Tooltips
$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$( '.float-label input' ).keyup(function() {
    // Check if float label input is not empty, if so then add some CSS
    if ( $(this).val().length > 0 ) {

        $(this).css({
            paddingTop: '1.2rem',
            paddingBottom: '.4rem'
        });

        $(this).next('label').css({
            top: '.3rem',
            fontSize: '75%'
        });

    };
});

// jquery stuff goes here
$(document).ready(function() {
    // Stepper input
    var $stepperInput = $('.stepper-input input');

    // Check if float label input has items, if so then add some CSS
    if ( $('.float-label .selectize-input').find('.item').length > 0 ) {
        $('.selectize-input').parent().next('label').css({
            top: '.3rem',
            fontSize: '75%'
        });
    };

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
});
