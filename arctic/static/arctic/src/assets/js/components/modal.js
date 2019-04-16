function modal_close() {
    if ('parentIFrame' in window) {
        window.parentIFrame.sendMessage('close');
    }
}

$(document).ready(function() {

    $('iframe').iFrameResize({
        scrolling: true,
        warningTimeout: 0,
        resizedCallback: function(messageData) {
            $('#iframe-modal').modal('handleUpdate');
        },
        messageCallback: function(messageData) {
            if (messageData.message == 'close') {
                $('#iframe-modal').modal('hide');
            }
        }
    });

    $('#confirm-dialog').on('show.bs.modal', function (event) {
        var modal = $(this);
        var button = $(event.relatedTarget); // Button that triggered the modal
        modal.addClass(button.data('confirm-class'));
        modal.find('.modal-title').text(button.data('confirm-title'));
        modal.find('.modal-body').html(button.data('confirm-message'));
        modal.find('.modal-footer .confirm-cancel').text(button.data('confirm-cancel'));
        modal.find('.modal-footer .confirm-ok').text(button.data('confirm-ok'));
        modal.find('.modal-footer .confirm-ok').prop('href', button.attr('href'));
    });

    $('#iframe-modal').on('show.bs.modal', function (event) {
        var modal = $(this)
        var button = $(event.relatedTarget) // Button that triggered the modal
        var size = button.data('size');
        var height = button.data('height');
        var url = button.prop('href');
        var prefix = '?';
        var urlArr = url.split('?')
        if (size == 'extra-large') {
            modal.find('.modal-dialog').addClass('modal-exlg');
        }
        if (size == 'large') {
            modal.find('.modal-dialog').addClass('modal-lg');
        }
        else if (size == 'small') {
            modal.find('.modal-dialog').addClass('modal-sm');
        }
        if (height) {
            modal.find('iframe').css('height', height);
        }
        //check if url already has parameters
        if (urlArr.length > 1 && urlArr[1] !== '') {
            prefix = '&';
        }
        modal.find('iframe').prop('src', url +  prefix + 'inmodal=True');
    });

    $('#iframe-modal').on('hidden.bs.modal', function (event) {
        $(this).find('iframe').prop('src', '');
    });
});
