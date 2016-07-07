// deps: js/utils/helpers.js
( function () {
    var element = $( 'input[name="slug"]' );
    var title = element.closest( '.row' ).prev().find( 'input[name="title"]' );

    if ( element.length && title.length ) {

        // only keep title and slug in sync when they have the same values
        if ( slugify( title.val() ) == element.val() ) {
            title.on( "keyup", function () {
                element.val( slugify( title.val() ) );
            } );
        }


        // when slug is manualy changed
        element.on( "keyup", function ( e ) {
            var code = e.which;

            //keycode 9 = tab
            if ( code == 9 ) {
                return;
            }

            title.off( "keyup" );
        } );


        // Is it edit or new?
        if ( element.val() != '' || title.val() != '' ) {

            // form is submitted
            element.closest( 'form' ).on( 'submit', function () {

                var currentTitle = slugify( title.val() );

                // are title and slug different?
                if ( currentTitle != element.val() ) {

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

