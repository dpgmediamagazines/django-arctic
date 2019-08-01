function show_artic_loader() {
    var loaderTemplate = `<div class="arctic-loader">
        <svg class="spinner-container" viewBox="0 0 44 44">
        <circle class="path" cx="22" cy="22" r="20" fill="none" stroke-width="4"></circle>
        </svg>
    </div>`;
    if (!$('.arctic-loader').length) {
        $('body').append(loaderTemplate);
    }
}

function hide_artic_loader() {
    $('.arctic-loader').remove();
}
