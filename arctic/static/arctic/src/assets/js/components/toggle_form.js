/* Toggle Form functionality. Wraps a form inside a popover. Used for advanced search. */

(function($) {
    $('.arctic_toggle_form_button').popover({
        container: 'body',
        content: function () {
            // copy
            var selector = $(this).data('popover_content_container');
            var contents = $(selector).contents().clone();

            // rewrite for and id attributes to guarantee uniqueness
            contents.find('[for]').each(function () {
                var attr = $(this).attr('for');
                $(this).attr('for', attr + '_in_advanced_search');
            });

            contents.find('[id]').each(function () {
                var attr = $(this).attr('id');
                $(this).attr('id', attr + '_in_advanced_search');
            });

            return contents;
        },
        html: true
    });
})(jQuery);