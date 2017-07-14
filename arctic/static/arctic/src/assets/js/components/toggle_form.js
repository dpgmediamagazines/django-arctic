/* Toggle Form functionality. Wraps a form inside a popover. Used for advanced search. */

(function($) {
    $('.arctic_toggle_form_button').each(function(){
        var selector = $(this).data('popover_content_container');
        var form = $(selector).contents();

        $(this).data('form', form);
    }).popover({
        content: function () {
            return $(this).data('form');
        },
        html: true
    });
})(jQuery);