function startSelectize() {
    $('[js-selectize]').each(function(index) {
        var instance = this;
        $(instance).selectize({
            allowEmptyOption: true,
            highlight: false,
            plugins: ['remove_button'],
            onFocus: function() {
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
                }
            },
            // Selectize reoders search results to find best match.
            // But we wan't to keep original order by default
            score: function() {
                return function() { return 1 };
            }
        });
    });
}

function startSelectizeMultiple() {
    $('[js-selectize-multiple]').each(function(index) {
        var instance = this;
        $(instance).selectize({
            delimiter: ',',
            persist: false,
            plugins: ['remove_button'],
            onFocus: function() {
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
                }
            },
            create: function(input) {
                return {
                    value: input,
                    text: input
                }
            },
            // Selectize reoders search results to find best match.
            // But we wan't to keep original order by default
            score: function() {
                return function() { return 1 };
            }
        });
    });
}

function startSelectizeAutocomplete() {
    $('[js-selectize-autocomplete]').each(function(index) {
        var instance = this
        var url = $(instance).attr('data-url');
        $(instance).selectize({
            valueField: 'value',
            labelField: 'label',
            searchField: 'label',
            create: false,
            load: function(query, callback) {
                if (!query.length) return callback();
                this.clearOptions();
                $.ajax({
                    url: url + encodeURIComponent(query),
                    type: 'GET',
                    error: function() {
                        callback();
                    },
                    success: function(res) {
                        callback(res.options);
                    }
                });
            },
            onFocus: function() {
                $(instance).next().next().css({
                    top: '.3rem',
                    fontSize: '75%'
                });
            },
            onBlur: function() {
                if ($(instance).next().find('.item').length == 0) {
                    $(instance).next().next().removeAttr('style');
                }
            },
        });
    });
}

function startAllSelectizes() {
    startSelectize();
    startSelectizeMultiple();
    startSelectizeAutocomplete();
}
