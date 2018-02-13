$(document).ready(function() {
    $('.float-label input, .float-label textarea').each(function() {
        if (($(this).val().length == 0) && ($(this).text() == 0)) {
            $(this).addClass('empty');
        }
    });
    
    $('.float-label input, .float-label textarea').blur(function() {
        // Check if float label input is not empty, if so then add some CSS
        if (($(this).val().length > 0) || ($(this).text() > 0)) {
            $(this).removeClass('empty');
        }
        else {
            $(this).addClass('empty');
        }
    });
    
    // Selectize controls
    $('.float-label .selectize-input').each(function() {
        if $(this).find('.item').length == 0) {
            $(this).addClass('empty');
        }
    }
    $('.float-label .selectize-input').blur(function() {
        if $(this).find('.item').length > 0) {
            $(this).removeClass('empty');
        }
        else {
            $(this).addClass('empty');
        }
    }


});
