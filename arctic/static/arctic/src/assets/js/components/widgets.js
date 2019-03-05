function startListSorting() {
    // sortable ListViews
    $('[data-sorting-url]').each(function(index) {
        var url = $(this).attr('data-sorting-url');
        var updated_items = new Object();
        Sortable.create(this, {
            handle: '.drag-handle',
            animation: 100,
            onUpdate: function (/**Event*/evt) {
                var base_sorting_value = 1;
                $(evt.to).find('.drag-handle i').each(function(index) {
                    var key = $(this).attr('data-sorting-key');
                    var value = $(this).attr('data-sorting-value');
                    if (parseInt(value) != base_sorting_value) {
                        updated_items[key] = base_sorting_value;
                        $(this).attr('data-sorting-value', base_sorting_value);
                    }
                    base_sorting_value += 1;
                });
                $.post(url, JSON.stringify(updated_items))
                .done(function() {
                    // keep this empty for now
                })
                .fail(function() {
                    console.error('Unable to post reordering to backend')
                })
            }
        });
    });

    $('[data-sorting-url] tr').on('dragstart', function(e) {
        $(this).css('opacity', '0.5');
        return true;
    });

    $('[data-sorting-url] tr').on('dragend', function(e) {
        $(this).css('opacity', 'inherit');
        return true;
    });
}

function startAllWidgets() {
    startAllSelectizes();
    startAllPickers();
    betterFile();
}


$(document).ready(function() {
    // Start all widgets fields
    startAllWidgets();

    // tooltips
    $('[data-toggle="tooltip"]').tooltip()

    //float labels
    floatLabels();

    // Sort lists
    startListSorting();

    // dynamic inlines...
    startAllInlines();
});
