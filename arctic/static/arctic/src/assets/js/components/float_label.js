function floatLabels() {
    $('.float-label input, .float-label textarea').each(function() {
        if (($(this).val().length == 0) && ($(this).text() == 0)) {
            $(this).addClass('empty');
            $(this).val('');
        }
    });

    $('.float-label input, .float-label textarea').off().on('blur', function() {
        // Check if float label input is not empty, if so then add some CSS
        if (($(this).val().length > 0) || ($(this).text().length > 0)) {
            $(this).removeClass('empty');
        }
        else {
            $(this).addClass('empty');
            $(this).val('');
        }
    });

    // Selectize controls
    $('.float-label .selectize-input.has-items').each(function() {
        // Check if float label input is not empty, if so then add some CSS
            $(this).css({
                paddingTop: '1.1rem',
                paddingBottom: '.1rem'
            });

            $(this).parent().next('label').css({
                top: '.3rem',
                fontSize: '75%'
            });
    });
}
