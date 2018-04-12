$(document).ready(function() {
    $('#confirm-dialog').on('show.bs.modal', function (event) {
        var modal = $(this)
        var button = $(event.relatedTarget) // Button that triggered the modal
        modal.addClass(button.data('confirm-class'));
        modal.find('.modal-title').text(button.data('confirm-title'));
        modal.find('.modal-body').text(button.data('confirm-message'));
        modal.find('.modal-footer .confirm-cancel').text(button.data('confirm-cancel'))
        modal.find('.modal-footer .confirm-ok').text(button.data('confirm-ok'))
        modal.find('.modal-footer .confirm-ok').prop('href', button.prop('href'));
    });
});
