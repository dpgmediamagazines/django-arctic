// deps: js/utils/helpers.js
( function () {

    // example:
    // <input data-to-slugify="input['title']" />

    var element = $( 'input[data-to-slugify]' );
    var target = $( element.data( 'to-slugify' ) );

    if ( element.length && target.length ) {

        // only keep target and slug in sync when they have the same values
        if ( slugify( target.val() ) == element.val() ) {
            target.on( "keyup", function () {
                element.val( slugify( target.val() ) );
            } );
        }


        // when slug is manualy changed
        element.on( "keyup", function ( e ) {
            var code = e.which;

            //keycode 9 = tab
            if ( code == 9 ) {
                return;
            }

            target.off( "keyup" );
        } );


        // Is it edit or new?
        if ( element.val() != '' || target.val() != '' ) {

            // form is submitted
            element.closest( 'form' ).on( 'submit', function () {

                var targetSlugified = slugify( target.val() );

                // are target and slug different?
                if ( targetSlugified != element.val() ) {

                    // it's changed, we need to confirm that
                    var msg;
                    msg = "Slug is aangepast";
                    if ( !confirm( msg ) ) {
                        return false;
                    }
                }
            } );
        }
    }
} )();

