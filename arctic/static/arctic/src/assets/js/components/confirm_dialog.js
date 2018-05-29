$(document).ready(function() {
    
    $('iframe').iFrameResize({
        scrolling: true,
        resizedCallback: function(messageData) {
            $('#iframe-modal').modal('handleUpdate');
        }
    });

    $('#confirm-dialog').on('show.bs.modal', function (event) {
        var modal = $(this)
        var button = $(event.relatedTarget) // Button that triggered the modal
        modal.addClass(button.data('confirm-class'));
        modal.find('.modal-title').text(button.data('confirm-title'));
        modal.find('.modal-body').html(button.data('confirm-message'));
        modal.find('.modal-footer .confirm-cancel').text(button.data('confirm-cancel'))
        modal.find('.modal-footer .confirm-ok').text(button.data('confirm-ok'))
        modal.find('.modal-footer .confirm-ok').prop('href', button.prop('href'));
    });

    $('#iframe-modal').on('show.bs.modal', function (event) {
        var modal = $(this)
        var button = $(event.relatedTarget) // Button that triggered the modal
        var size = button.data('size');
        if (size == 'large') {
            modal.find('.modal-dialog').addClass('modal-lg');
        }
        else if (size == 'small') {
            modal.find('.modal-dialog').addClass('modal-sm'); 
        }
        modal.find('iframe').prop('src', button.prop('href'));
    });

    $('#iframe-modal').on('hidden.bs.modal', function (e) {
        window.location.reload(false);        
    })

});
