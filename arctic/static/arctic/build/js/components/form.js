// deps: js/utils/helpers.js
( function () {
    var element = $( 'input[name="slug"]' );
    var title = element.closest( '.row' ).prev().find( 'input[name="title"]' );

    // create slugified title
    title.on( "keyup", function () {
        element.val( slugify( title.val() ) );
    } );

    // validate title or slug change
    if ( element.val() != '' || title.val() != '' ) {

        // save init values
        var initelementVal = element.val()
        var initTitleVal = title.val()

        // submit is clicked
        element.closest( 'form' ).on( 'submit', function () {

            // compare init values to current values
            if ( initelementVal != element.val() || initTitleVal != title.val ) {

                var msg;

                // set a message to confirm
                if ( initelementVal != element.val() ) {
                    msg = "Slug is aangepast";
                }

                if ( initTitleVal != title.val() ) {
                    msg = "Titel is aangepast";
                }

                // confirm changes
                if ( !confirm( msg ) ) {
                    return false;
                }
            }
        } );
    }
} )();

