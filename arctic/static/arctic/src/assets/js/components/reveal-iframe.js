/*

    Reveal.js extends foundation reveal()

    When triggering a dialog
    <element data-url />  = is url which need to be opened with iframe
    <element data-size /> = size of dialog

    Closing dialog within iframe
    <body data=auto-close /> = closes dialog
    <body data=refresh-parent /> = refresh parent window
    <element data-close-dialog /> = onclick closes dialog
 */

( function ( $ ) {

    "use strict";

    // template and state
    var dialog = {};
    dialog.element = '<section id="reveal-iframe" class="reveal external" data-reveal><iframe frameborder="0" allowfullscreen></iframe></section>';
    dialog.element = $( dialog.element );
    dialog.parameter = 'dialog=1';
    dialog.size = null;
    dialog.url = null;
    dialog.ready = false;
    dialog.extraScrollHeight = 20;


    // dialog methods
    var isDialog = {

        init( $triggers ) {
            var self = this;

            if ( !$triggers instanceof jQuery ) {
                throw new Error( '$triggers is not a jQuery object' );
                return
            }

            self.listeners( $triggers );
        },

        listeners: function( $triggers ) {
            var self = this;

            // open dialog with trigger properties
            $triggers.on( 'click', function ( event ) {
                event.preventDefault();

                var trigger = $( this );
                dialog.url = trigger.data( 'url' );
                dialog.size = trigger.data( 'size' );

                // foundation opens dialog cause 'data-open' attr, which triggers 'open.zf.reveal'

                // setup iframe
                dialog.open( dialog.url, dialog.size );
            });

            // reset iframe when foundation when closing
            dialog.element.on( 'closed.zf.reveal', function() {
                dialog.close();
            });
        },
    }


    // methods when loaded within dialog iframe
    var inDialog = {

        init: function( $body ) {
            var self = this;
            self.setup( $body );
            self.listeners( $body );
        },


        setup: function( $body ) {
            var self = this;

            self.linksToDialog( $body );
        },


        // give links isDialog parameter so it opens in dialog layout
        linksToDialog: function( $body ) {
            var anchors = $body.find( 'a' );

            if ( !anchors.length ) {
                return
            }

            for ( var i = 0; i < anchors.length; i++ ) {
                var anchor = $( anchors[i] );
                var url = anchor.attr( 'href' );

                if ( url != undefined && url.length ) {

                    // check if url contains '?'
                    if ( url.match(/\?./) ) {
                        url = url + '&' + dialog.parameter;
                    } else {
                        url = url + '?' + dialog.parameter;
                    }

                    anchor.attr( 'href', url );
                }
            }
        },


        isUrlParameter: function ( url, field ) {
            if(url.indexOf('?' + field + '=') != -1)
                return true;
            else if(url.indexOf('&' + field + '=') != -1)
                return true;
            return false
        },


        listeners: function( $body ) {
            var self = this;

            // auto close from within iframe
            var refreshParent = $body.data( 'refresh-parent' );
            if ( refreshParent ) {
                window.parent.location.reload();
            };

            // find dialog..
            if ( window.parent === window ) {
                self.dialog = $( 'body' ).find( '.reveal' );
            } else {
                self.dialog = window.parent.$( window.parent.document ).find( '.reveal' );
            }

            // auto close
            var autoClose = $body.data( 'auto-close' );
            if ( autoClose ) {
                self.dialog.foundation( 'close' );
            };

            // close on click
            var buttons = $body.find( '[data-close-dialog]' );
            buttons.on( 'click' , function ( event ) {

                // is previous page within iframe, then go back..
                if ( document.referrer.length ) {

                    var referrerUrl = document.referrer;
                    var referrerIsDialog = self.isUrlParameter( referrerUrl, 'dialog' );

                    if ( referrerIsDialog ) {
                        history.back();
                        return
                    }
                }

                // else close dialog..
                event.preventDefault();
                self.dialog.foundation( 'close' );
                buttons.off( 'click' );
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
        // * foundation opens dialog
        open: function( url, size ) {
            var self = this;
            dialog.ready = false;
            self.setDialogSize( size );
            self.setIframeSrc( url, self.setIframeDimensions );
        },


        // set dialog size with as default tiny
        setDialogSize: function ( size ) {
            var self = this;

            if ( size !== undefined && size.length ) {
                self.dialog.addClass( size );
            } else {
                self.dialog.addClass( 'tiny' ); // set default size when there's null..
            }
        },


        // set iframe src with an callback to fire when finish loading
        setIframeSrc: function ( url, callback ) {
            var self = this;
            var iframe = self.dialog.find( 'iframe' );

            iframe.load( function() {
                if ( !dialog.ready ) {
                    dialog.ready = true;
                    callback( self )
                }
            }).attr( "src", url );
        },


        // set dimensions of iframe
        setIframeDimensions: function ( self ) {
            var iframe = self.dialog.find( 'iframe' );

            // container with overflow scroll
            var $wrapper = iframe.contents().find( ".block-wrapper" );
            var scrollHeight = $wrapper[0].scrollHeight;

            // set height
            iframe.css( 'height', scrollHeight + self.extraScrollHeight );

            // trigger resize for positioning
            $( window ).trigger( 'resize' );
        },


        // close dialog
        // * foundation closes dialog
        close: function() {
            var self = this;
            self.disableAreYouSure();
            self.removeIframeMarkUp();
            self.removeDialogSizes();
        },


        // disable areYouSure in iframe before closing dialog..
        disableAreYouSure: function() {
            var self = this;
            var iframe = self.dialog.find( 'iframe' );

            var form = iframe.contents().find( '.dirty-check' );
            form.removeClass( 'dirty' );
            form.areYouSure( { 'silent':true } );
        },


        removeIframeMarkUp: function() {
            var self = this;

            self.dialog.find( 'iframe' )
                .removeAttr( 'style' )
                .removeAttr( 'src' );
        },


        // remove possible already setted sizes
        removeDialogSizes() {
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
    $( document ).ready( function() {
        var $body = $( 'body.dialog' );
        var $triggers = $( '[data-open][data-url]' );

        if ( $triggers.length ) {
            dialog.setup();
            isDialog.init( $triggers );
        } else if ( $body.length ) {
            inDialog.init( $body );
        }
    });

})( jQuery );