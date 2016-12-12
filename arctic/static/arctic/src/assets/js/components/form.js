// deps: js/utils/helpers.js
( function () {

    // example:
    // <input data-to-slugify="input['title']" />

    var element = $( 'input[data-to-slugify]' );
    var target = $( element.data( 'to-slugify' ) );

    var elementVal = element.val();
    var targetVal = target.val();


    if ( element.length && target.length ) {

        var targetValCache = targetVal;

        target.on( "keyup", function () {
            var currentTargetVal = target.val()

            // check if it really is a change
            if ( targetValCache == currentTargetVal ) {
                return;
            } else {
                targetValCache = currentTargetVal;
            }

            // there's a change update slug
            element.val( arctic.utils.slugify( target.val() ) );
        } );


        // Is it edit or new?
        if ( element.val() != '' || target.val() != '' ) {

            // form is submitted
            element.closest( 'form' ).on( 'submit', function () {

                var targetSlugified = arctic.utils.slugify( target.val() );

                // are element or target updated ?
                if ( elementVal != element.val() || targetVal != target.val() ) {

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