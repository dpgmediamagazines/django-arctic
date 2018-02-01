$(document).ready(function() {
    $('.float-label input, .float-label textarea').blur(function() {
        // Check if float label input is not empty, if so then add some CSS
        if (($(this).val().length > 0) || ($(this).text() > 0)) {
            $(this).removeClass('empty');
            alert('not empty');
        }
        else {
            $(this).addClass('empty');
            alert('empty');
        }
    });
    
    // Check if float label input has items, if so then add some CSS
    if ($('.float-label .selectize-input').find('.item').length > 0) {
        $('.selectize-input').parent().next('label').css({
            top: '.3rem',
            fontSize: '75%'
        });
    }
});
