
/*
    Reveal.js extends foundation reveal()

    Required html attributes:
    data-open = is unique id for dialog
    data-url = is url which need to be opened with iframe
 */

( function ( $ ) {

    'use strict';

    function RevealIframe( element ) {
        this.element = element;

        // setup dialog with iframe listener
        if ( this.element && this.element.size() ) {
            this.location = window.location.href;
            this.id = this.element.data( 'open' );
            this.dialog = $( '#' + this.id );
            this.iframe = this.dialog.find( 'iframe' );

            // dialog arguments
            this.url = this.element.data( 'url' );
            this.size = this.element.data( 'size' );

            this.init();
        }

        // script is loaded witin an iframe
        if ( window.parent != window ) {
            this.framed = true;
            this.autoClose = this.element.data( 'auto-close' );
            this.parentReload = $('body').data( 'refresh-parent' );
            this.hideButton = $( '[data-close]' );

            this.initFramed();
        }

        var self = this;
    }


    // setup listner to trigger dialog
    RevealIframe.prototype.init = function ( ) {
        var self = this;

        // is there a dialog and a element?
        if ( self.dialog && self.element.size() ) {

            // when element clicked opend dialog
            self.element.on( 'click', function ( event ) {
                event.preventDefault();

                // add sizing class
                if ( self.size ) {
                    self.dialog.addClass( self.size );
                }

                // open dialog
                self.open( self.url );
            })
        }
    }


    // check when to close dialog from it's self
    RevealIframe.prototype.initFramed = function ( ) {
        var self = this;

        // if in iframe listen to close dialog
        if ( self.framed ) {

            // auto close from within iframe
            if ( self.parentReload ) {
                window.parent.location.reload();
            }

            // auto close from parent
            if ( self.autoClose ) {
                self.close( );
            }

            // close on click
            self.hideButton.on( 'click' , function ( ) {
                self.close( );
            })
        }
    }


    // opens a dialog
    RevealIframe.prototype.open = function ( url ) {
        var self = this

        // listsen to foundation event to open dialog
        self.dialog.on( 'open.zf.reveal', function ( ) {

            // setup correct url
            self.iframe.attr( 'src', url );

            // setup iframe height
            self.iframe.on( 'load' , function( ) {
                var offset = 200;
                var height = window.innerHeight;

                this.style.height = height - offset + 'px';
            })
        })

        this.dialog.trigger('open.zf.reveal');
    }


    // closes dialog
    RevealIframe.prototype.close = function ( ) {
        var self = this

        // find all dialogs
        self.dialog = window.parent.$( window.parent.document).find( '.reveal' )

        // triggers an close event to all dialogs
        self.dialog.trigger('closeme.zf.reveal');

        // get dialog iframe
        self.iframe = self.dialog.find('iframe');

        // disable areYouSure in iframe before removing src
        self.form = this.iframe.contents().find( '.dirty-check' );
        self.form.removeClass( 'dirty' );
        self.form.areYouSure( {'silent':true} );

        // remove src on iframe
        self.iframe.removeAttr( 'src' );
    }


    // initiate
    new RevealIframe( $( '[data-open][data-url], [data-open][data-auto-close]' ) );
})( jQuery );