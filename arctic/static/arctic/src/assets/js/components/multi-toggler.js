( function ( $ ) {

    function Toggler( element ) {

        if ( element instanceof jQuery ) {
            this.element = element
        } else {
            throw new Error( 'toggler expects a jQuery object' )
        }

        var self = this
        self.init()
    }

    Toggler.prototype.init = function ( ) {
        var self = this

        // loop through all selected instances and create a click listener
        $.each( self.element, function( index, clicked ) {
            self.clicked = $( clicked )

            self.clicked.on( 'click', function ( ) {
                self.toggle( index )
            })
        })
    }

    Toggler.prototype.toggle = function ( index ) {
        var self = this

        // get clicked element as a jQuery object
        self.clicked =  $( self.element[ index ] );

        // select elements who needs to be openend en closed
        self.open = self.clicked.data( 'open' )
        self.close = self.clicked.data( 'close' )

        if ( self.open ) {
            self.open = $( '#' + self.open )
        }
        if ( self.close ) {
            self.close = $( '#' + self.close )
        }

        // get toggler classes
        self.open.toggleClass = self.open.data( 'toggler' )
        self.close.toggleClass = self.open.data( 'toggler' )

        // show and hide element
        self.open.removeClass( self.open.toggleClass )
        self.close.addClass( self.close.toggleClass )

        self.element.removeClass( 'is-active' )
        self.clicked.addClass( 'is-active' )
    }

    $( document ).ready( function() {
        var element = $( '[data-multi-toggler][data-open][data-close]' )
        new Toggler( element )
    })
} )( jQuery )