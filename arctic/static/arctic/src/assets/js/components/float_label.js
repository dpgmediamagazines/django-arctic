$(document).ready(function() {
    $('.float-label input, .float-label textarea').each(function() {
        if (($(this).val().length == 0) && ($(this).text() == 0)) {
            $(this).addClass('empty');
            $(this).val('');
        }
    });
    
    $('.float-label input, .float-label textarea').blur(function() {
        // Check if float label input is not empty, if so then add some CSS
        if (($(this).val().length > 0) || ($(this).text() > 0)) {
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
                paddingTop: '1.2rem',
                paddingBottom: '.4rem'
            });

            $(this).parent().next('label').css({
                top: '.3rem',
                fontSize: '75%'
            });
    });
    $('.float-label .selectize-input.has-items').blur(function() {
        // Check if float label input is not empty, if so then add some CSS
        if ($(this).val().length > 0) {
            $(this).css({
                paddingTop: '1.2rem',
                paddingBottom: '.4rem'
            });

            $(this).next('label').css({
                top: '.3rem',
                fontSize: '75%'
            });
        }
    });
});
