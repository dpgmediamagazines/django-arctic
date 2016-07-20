"use strict";

( function() {

    var name = '.rule-builder';
    var element = $( name );

    // get data
    var filters = element.data( 'filters' );

    // init querybuilder
    element.queryBuilder({
        icons: {
            add_group: 'fa fa-plus-square',
            add_rule: 'fa fa-plus-circle',
            remove_group: 'fa fa-minus-square',
            remove_rule: 'fa fa-minus-circle',
            error: 'fa fa-exclamation-triangle'
        },
        allow_groups: 1,
        filters: filters
    });

    // get form elements
    var form = element.closest('form');
    var submit = form.find('[type="submit"]');

    // save rules
    submit.on('click', function( event ) {
        var result = element.queryBuilder('getRules');

        if (!$.isEmptyObject(result)) {
            $('#id_conditions').val(JSON.stringify(result, null, 2));
        }
    });

}) ();