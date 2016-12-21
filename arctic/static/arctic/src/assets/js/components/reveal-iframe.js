/*
    Reveal.js extends foundation reveal()

    When triggering a dialog
    data-open = is unique id for dialog
    data-url = is url which need to be opened with iframe
    data-size = size of dialog

    Closing dialog within iframe
    <body data=auto-close /> = close dialog
    <body data=refresh-parent = refresh parent window
    data-close = onclick closes dialog
 */

( function ( $ ) {

    "use strict";

    // template and state
    var dialog = {};
    dialog.element = '<section id="reveal-iframe" class="reveal external" data-reveal><iframe frameborder="0" allowfullscreen></iframe></section>';
    dialog.element = $( dialog.element );
    dialog.size = null;
    dialog.url = null;


    // dialog methods
    var isDialog = {

        init( $triggers ) {
            var self = this;
            self.listeners( $triggers );
        },

        listeners: function( $triggers ) {
            var self = this;

            if ( !$triggers instanceof jQuery ) {
                throw new Error( '$triggers is not a jQuery object' );
                return
            }

            // get dialog properties from element $trigger
            $triggers.on( 'click', function ( event ) {
                event.preventDefault();

                var trigger = $( this );
                dialog.url = trigger.data( 'url' );
                dialog.size = trigger.data( 'size' );
            });

            // set iframe src and size when foundation is ready..
            dialog.element.on( 'open.zf.reveal', function() {
                dialog.open( dialog.url, dialog.size );
            });

            // reset iframe when foundation is ready..
            dialog.element.on( 'closed.zf.reveal closeme.zf.reveal', function() {
                dialog.close();
            });
        },
    }


    // methods when loaded within dialog iframe
    var inDialog = {

        init: function( $body ) {
            var self = this;
            self.listeners( $body );
        },

        listeners: function( $body ) {
            var self = this;

            // auto close from within iframe
            var refreshParent = $body.data( 'refresh-parent' );
            if ( refreshParent ) {
                window.parent.location.reload();
            };

            // auto close
            var autoClose = $body.data( 'auto-close' );
            if ( autoClose ) {
                dialog.close();
            };

            // close on click
            var buttons = $body.find( '[data-close]' );
            buttons.on( 'click' , function ( event ) {
                event.preventDefault();

                // find dialog..
                if ( window.parent === window ) {
                    self.dialog = $( 'body' ).find( '.reveal' );
                } else {
                    self.dialog = window.parent.$( window.parent.document ).find( '.reveal' );
                }

                // triggers an close event to all dialogs
                self.dialog.foundation( 'close' );

                // disable listeners
                $( '[data-close]' ).off( 'click' );
            });
        }
    };


    // generic dialog methods
    $.extend( dialog, {

        // setup dialog by adding dialog template into DOM
        setup: function() {
            var self = this;

            self.dialog = self.element;
            $( 'body' ).append( self.dialog );
            new Foundation.Reveal( self.dialog );
        },

        // open dialog
        open: function( url, size ) {
            var self = this;

            // foundation opens dialog..

            self.removeSize();

            // set dialog size
            if ( size.length ) {
                self.dialog.addClass( size );
            } else {
                self.dialog.addClass( 'small' ); // set default size when there's null..
            }

            // set iframe src
            var iframe = self.dialog.find( 'iframe' );
            iframe.attr( 'src', url );

            // setup iframe height to fit content
            // not heigher then parent window!
            iframe.on( 'load' , function( ) {
                var offset = 200;
                var height = window.innerHeight;

                this.style.height = height - offset + 'px';
            })
        },

        // close dialog
        close: function() {
            var self = this;

            // foundation closes dialog..
            self.removeSize();
        },

        // remove possible already setted sizes
        removeSize: function () {
            var self = this;

            // possible sizes
            var sizes = [ 'tiny', 'small', 'large', 'full' ];

            // remove one by one
            for ( var i = 0; i < sizes.length; i++ ) {
                self.dialog.removeClass( sizes[i] );
            }
        },

        // completely remove iframe dialog and listeners
        destroy: function( $triggers ) {
            var self = this;

            // remove dialog
            self.dialog.remove();

            // disable listeners
            self.dialog.off( 'open.zf.reveal' );
            self.dialog.off( 'close.zf.reveal' );

            if ( $triggers.length ) {

                if ( !$triggers instanceof jQuery ) {
                    throw new Error( '$triggers is not a jQuery object' );
                    return
                }

                $triggers.off( 'click' );
            }
        }
    });


    // public methods
    window.arctic.utils.revealInIframe = {
        setup: function() {
            dialog.setup();
        },
        open: function( url, size ) {
            dialog.element.foundation( 'open' );
            dialog.open( url, size );
        },
        close: function() {
            dialog.close();
        }
    }


    // init module
    var $body = $( 'body.dialog' );
    var $triggers = $( '[data-open][data-url]' );

    if ( $triggers.length ) {
        dialog.setup();
        isDialog.init( $triggers );
    } else if ( $body.length ) {
        inDialog.init( $body );
    }

})( jQuery );