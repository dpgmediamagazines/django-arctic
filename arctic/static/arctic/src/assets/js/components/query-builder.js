"use strict";

$( document ).ready(function() {

    // required fields
    var element = $( '.query-builder' );

    // get filters var name and value
    var filters_var = element.data('filters-var');
    var filters = window[filters_var];

    if ( element.size() && filters !== undefined ) {

        // settings
        var settings = {};
        settings.icons = {
            add_group: 'fa fa-plus-square',
            add_rule: 'fa fa-plus-circle',
            remove_group: 'fa fa-minus-square',
            remove_rule: 'fa fa-minus-circle',
            error: 'fa fa-exclamation-triangle'
        }
        settings.allow_groups = 1;
        settings.filters = filters;

        // get conditions var name and value
        var conditions_var = element.data('conditions-var');
        var conditions;

        // define conditions if there's an value
        if (typeof conditions_var !== 'undefined') {
            conditions = window[conditions_var];
            settings.rules = conditions;
        }

        // init querybuilder
        element.queryBuilder( settings );

        // get form elements
        var form = element.closest( 'form' );
        var submit = form.find( '[type="submit"]' );

        // save rules
        submit.on( 'click', function ( event ) {
            var result = element.queryBuilder( 'getRules' );

            if ( !$.isEmptyObject( result ) ) {
                $( '#id_conditions' ).val( JSON.stringify( result, null, 2 ) );
            }
        } );
    }
});