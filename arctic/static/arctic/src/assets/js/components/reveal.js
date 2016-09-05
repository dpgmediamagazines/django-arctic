function Reveal( element ) {
    this.element = element

    // all close buttons
    this.hide = $( '[data-close]' )

    // set these variables when there's an element
    if ( this.element && this.element.size() ) {
        this.url = this.element.data( 'url' )
        this.id = this.element.data( 'open' )
        this.dialog = $( '#' + this.id )
        this.iframe = this.dialog.find('iframe')
    }

    // it's an iframe
    if ( window.parent != window ) {
        this.framed = true;
        this.body = $( 'body' );
        this.id = this.body.data( 'id' )
        this.auto_close = this.body.data( 'auto-close' )
    }

    self = this
    this.init()
}


Reveal.prototype.init = function ( ) {

    // listen to open dialog with an iframe
    if ( this.url && this.dialog && this.element.size() ) {
        this.element.on( 'click', this.open )
    }

    // if in iframe listen to close dialog
    if ( this.framed == true ) {

        if ( this.auto_close ) {
            this.close( this.id )
        }

        this.hide.on( 'click' , function ( ) {
            self.close( this.id )
        })
    }
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
    this.iframe = this.dialog.find('iframe')
    this.iframe.removeAttr( 'src' );
}


// initiate
new Reveal( $( '[data-open][data-url]' ) )