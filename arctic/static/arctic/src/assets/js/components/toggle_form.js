/* Toggle Form functionality. Wraps a form inside a popover. Used for advanced search. */

(function($) {
    var container = ''

    $('.arctic_toggle_form_button').off('click.advancedForm').on('click.advancedForm', function() {
        container = $(this).data('popover-container');
        if (!$(container).hasClass('hide')) {
            hidePopover(container);
            return;
        }
        $(container).removeClass('hide');
        $(this).attr('aria-describedby', 'true');
        setPosition();
        setTimeout(function(){ dismissOnClick(container); }, 0);
    });

    var setPosition = function () {
        if (!$('.arctic_toggle_form_button').length) {
            return false;
        }
        $(container).removeAttr('style');
        var $arrow = $(container).find('.arrow');
        $arrow.removeAttr('style');
        var marginRight = 24;
        var buttonPosition = $('.arctic_toggle_form_button')[0].getBoundingClientRect()
        var offset = $(container)[0].getBoundingClientRect();
        var windowWidth = document.documentElement.clientWidth;
        var newTop = offset.top - buttonPosition.top + buttonPosition.height;

        if (offset.top < buttonPosition.top) {
            newTop = buttonPosition.top - offset.top + buttonPosition.height + 2;
        }

        var newLeft = Math.abs(offset.left - (windowWidth - offset.width - marginRight));
        var translateProp = 'translate(' + newLeft + 'px, ' + newTop + 'px)';

        $(container).css({
            'position': 'absolute',
            'transform': translateProp,
        });

        //calculate arrow position
        var arrowOffset = $arrow[0].getBoundingClientRect();
        var newLeft = buttonPosition.left - arrowOffset.left + buttonPosition.width/2 - 3;
        $($arrow).css({
            'left': newLeft + 'px',
        });

        $(container).addClass('visible');
    };

    var hidePopover = function(container) {
        $('body').off('click.popover');
        $(container).addClass('hide');
        $(container).addClass('visible');
        $(container).removeAttr('style');
        $('.arctic_toggle_form_button').removeAttr('aria-describedby');
    };

    var checkIfDatepicker = function ($target) {
        if ($target.attr('class').indexOf('datepicker') > -1) {
            return true;
        } else {
            return false;
        }
    };

    var dismissOnClick = function () {
        $('body').off('click.popover').on('click.popover', function(e) {
            var target = e.target;
            if (!$(target).is('.popover') &&
                !$(target).parents().is('.popover') &&
                !$(target).is('.arctic_toggle_form_button') &&
                !$(target).parents().is('.arctic_toggle_form_button')
                ) {
                    //check if it's a datepicker container
                if (!checkIfDatepicker($(target))) {
                    hidePopover(container);
                }
            }
        });
    };

    var resizeTimeout = false;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(setPosition(), 250);
    });

    // Make popover visible in case advanced search form errors
    var hasAdvancedSearchErrors = $('#arctic_advanced_search').find('.invalid-form-field, .invalid-feedback').length > 0;
    if (hasAdvancedSearchErrors) {
        $('#arctic_toggle_advanced_search_form_button').click();
    }
})(jQuery);
