!(function(w, $) {
    //Mobile menu controls
    $('#menu-button').click(function(e) {
        $(this).toggleClass('is-active');
        $('.row-offcanvas').toggleClass('active');
        e.preventDefault();
    });

    let collapseButton = document.querySelectorAll('[js--collapse-menu]');

    for (var i = 0; i < collapseButton.length; i++) {
        collapseButton[i].addEventListener('click', function(event) {
            event.preventDefault();
            let el = this.querySelector('[js--collapse-menu-arrow]');

            this.classList.toggle('active');
            if (el.classList.contains('fa-angle-down')) {
                el.classList.remove('fa-angle-down');
                el.classList.add('fa-angle-left');
            } else {
                el.classList.add('fa-angle-down');
                el.classList.remove('fa-angle-left');
            }
            this.nextSibling.nextSibling.classList.toggle('active');
        });
    }
})(window, $);
//Turn on Tooltips
$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});


// jquery stuff goes here
$(document).ready(function() {
    var dirty_check = $('form.dirty-check');
    if (dirty_check.length && !window.parent != window) {
        dirty_check.areYouSure();

        $('form').on('dirty.areYouSure', function() {
            var tab = $('.tabs-title.is-active a')[0];
            if (tab && tab.text[0] != '●') { 
                tab.text = '● ' + tab.text;
            }
            document.title = '● ' + document.title;
        });

        $('form').on('clean.areYouSure', function() {
            var tab = $('.tabs-title.is-active a')[0];
            if (tab) {
                tab.text = tab.text.slice(2);
            }
            document.title = document.title.slice(2);
        });
    }

    // Search input by clicking on Icon
    var $searchIcon = $('[js-search-submit]');
    $searchIcon.on('click',  function (){
        $('form.search-form').submit();
    })
});

function select_quick_filter(self) {
    var next_input = $(self).next('input');
    next_input.attr('checked', true);
    $('form.search-form').submit();
}
