
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
        }

        // it's an iframe
        if ( window.parent != window ) {
            this.framed = true;
            this.parent = window.parent;
            this.body = $( 'body' );
            this.auto_close = this.element.data( 'auto-close' );
            this.parent_reload = $('body').data( 'refresh-parent' );
            this.hide = $( '[data-close]' );
        }

        var self = this;
        this.init();
    }


    RevealIframe.prototype.init = function ( ) {

        // open dialog with an iframe
        if ( this.dialog && this.element.size() ) {

            this.element.on( 'click', function ( event ) {
                event.preventDefault();

                self.url = $(this).data( 'url' );
                self.id = $(this).data( 'open' );
                self.size = $(this).data( 'size' );

                if ( this.size ) {
                    this.dialog.addClass( this.size );
                }

                self.open( self.url );
            })
        }

        // if in iframe listen to close dialog
        if ( this.framed ) {

            if ( this.parent_reload ) {
                this.parent.location.reload();
            }

            if ( this.auto_close ) {
                this.close( );
            }

            this.hide.on( 'click' , function ( ) {
                self.close( );
            })
        }
    }


    RevealIframe.prototype.open = function ( url ) {
        // setup iframe

        self.dialog.on( 'open.zf.reveal', function ( ) {
            self.iframe.attr( 'src', url );

            self.iframe.on( 'load' , function( ) {
                this.style.height = this.contentDocument.body.scrollHeight +'px';
            })
        })

        this.dialog.trigger('open.zf.reveal');
    }


    RevealIframe.prototype.close = function ( ) {

        // close all dialogs in parent window
        this.dialog = this.parent.$( window.parent.document).find( '.reveal' )

        // close all reveal dialogs within parent window
        this.dialog.trigger('closeme.zf.reveal');

        this.iframe = this.dialog.find('iframe');

        // disable areYouSure in iframe before removing src
        this.form = this.iframe.contents().find( '.dirty-check' );
        this.form.removeClass( 'dirty' );
        this.form.areYouSure( {'silent':true} );

        // remove src on iframe
        this.iframe.removeAttr( 'src' );
    }


    // initiate
    new RevealIframe( $( '[data-open][data-url], [data-open][data-auto-close]' ) );

})( jQuery );