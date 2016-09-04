function Reveal( element ) {
    this.element = element
    this.hide = $( '[data-close]' )

    // set these variables when there's an element
    if ( this.element && this.element.size() ) {
        this.id = this.element.data( 'open' )
        this.dialog = $( '#' + this.id )
        this.url = this.element.data( 'url' )
        this.iframe = this.dialog.find('iframe')
    }

    self = this
    this.init()
}


Reveal.prototype.init = function ( ) {

    // if required vars are set then initiate
    if ( this.url && this.dialog && this.element.size() ) {
        this.element.on( 'click', this.open )
    }

    // close dialog within iframe
    if ( this.hide.size() && window.parent != window ) {

        // button
        this.hide.on( 'click' , function ( ) {

            // get parent dialog id
            self.id = $( this ).closest( '.iframe.base' ).data( 'close' );

            // close dialog with id
            self.close( self.id )
        })
    } // else {  default foundation behaviour }
}


Reveal.prototype.open = function () {
    // set url
    self.iframe.attr( 'src', self.url )
}


Reveal.prototype.close = function ( id ) {

    if ( id ) {
        // if there's a ID only close this dialog in parent window
        this.dialog = window.parent.$( window.parent.document).find( '#' + id )
    } else {
        // close all dialogs in parent window
        this.dialog = window.parent.$( window.parent.document).find( '.reveal' )
    }

    // close all reveal dialogs within parent window
    this.dialog.trigger('closeme.zf.reveal');

    // remove src on iframe
    this.dialog.removeAttr( 'src' );
}


// initiate
new Reveal( $( '[data-open][data-url]' ) )