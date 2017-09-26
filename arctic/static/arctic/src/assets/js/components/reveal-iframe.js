/*

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
    dialog.element ='<div class="modal fade" id="revealModal" tabindex="-1" role="dialog" aria-labelledby="revealModalLabel" aria-hidden="true">' +
                    '<div class="modal-dialog" style="top:10%" role="document">' +
                    '<iframe frameborder="0" allowfullscreen></iframe>' +
                    '</div></div>';
    dialog.element = $( dialog.element );
    dialog.parameter = 'dialog=1';
    dialog.size = null;
    dialog.url = null;
    dialog.ready = false;


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
                dialog.minHeight = trigger.data( 'min-height' );

                // bootstarp opens dialog cause 'data-open' attr, which triggers 'open.zf.reveal'

                // setup iframe
                dialog.open(dialog.url, dialog.size, dialog.minHeight);
            });

            // reset iframe when bootstarp when closing from outside the dialog
            dialog.element.on( 'hidden.bs.modal', function() {
                dialog.close();
            });
        }
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
                self.dialog = $( 'body' ).find( '.modal' );
            } else {
                self.dialog = window.parent.$( window.parent.document ).find( '.modal' );
            }

            // auto close
            var autoClose = $body.data( 'auto-close' );
            if ( autoClose ) {
                self.dialog.modal('hide');
            };

            // close on click
            var buttons = $body.find( '[data-go-back-dialog]' );
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
                self.dialog.modal('hide');
                buttons.off('click');
            });
            var closeButton = $body.find( '[data-close-dialog]' );
            closeButton.on( 'click' , function ( event ) {
                event.preventDefault();
                self.dialog.modal( 'hide' );
                closeButton.off('click');
            });
        }
    };


    // generic dialog methods
    $.extend( dialog, {


        // setup dialog by adding dialog template into DOM
        addDialog: function() {
            var self = this;

            var hasDialog = $( 'body' ).find( self.dialog ).length;

            if ( hasDialog == 0 ) {
                self.dialog = self.element;
                $( 'body' ).find( self.dialog );
                //needs the timeout if the open animation is off
                setTimeout(function(){ self.dialog.modal('show'); }, 0);
            }
        },

        // open dialog
        open: function(url, size, minHeight) {
            var self = this;

            self.addDialog();
            dialog.ready = false;
            self.setDialogSize( size );
            self.setIframeSrc( url, self.setIframeDimensions, minHeight);
        },


        // set dialog size
        setDialogSize: function ( size ) {
            var self = this;

            if ( size !== undefined && size.length ) {
                self.dialog.addClass(size);
            }
        },


        // set iframe src with an callback to fire when finish loading
        setIframeSrc: function (url, callback, minHeight) {
            var self = this;

            var iframe = self.dialog.find( 'iframe' );
            iframe.on("load", function() {
                if ( !dialog.ready ) {
                    dialog.ready = true;
                    callback(self, minHeight)
                }
            });
            iframe.attr( "src", url );
        },


        // set dimensions of iframe
        setIframeDimensions: function (self, minHeight) {
            var iframe = self.dialog.find( 'iframe' );

            if (minHeight) {
                iframe.css( 'height', minHeight );
                self.repositionIframe(iframe);
            } else {
                // container with overflow scroll
                setTimeout(function(){
                    var $wrapper = iframe.contents().find( ".js--dialog-scrol-size" );
                    var scrollHeight = $wrapper[0].scrollHeight;

                    // set height
                    iframe.css( 'height', scrollHeight);
                    self.repositionIframe(iframe);
                }, 0);
            }
            // trigger resize for positioning
            $( window ).trigger( 'resize' );
        },

        repositionIframe: function (iframe) {
            var frameHeight = iframe.height();
            var windowHeight = window.innerHeight;
            var top = (windowHeight - frameHeight)/2;
            iframe.parent().css( 'top', top );
        },

        // close dialog
        // * bootstarp closes dialog
        close: function() {
            var self = this;
            self.disableAreYouSure();
            self.removeIframeMarkUp();
            self.removeDialogSizes();
            // self.removeDialog();
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
            self.dialog.off( 'shown.bs.modal' );
            self.dialog.off( 'hidden.bs.modal' );

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
        open: function( url, size ) {
            dialog.open( url, size );
            dialog.element.modal( 'show' );
        },
        close: function() {
            dialog.close();
        }
    }


    // init module
    $( document ).ready( function() {
        var $body = $( 'body.dialog' );
        var $triggers = $( '[data-target][data-url]' );

        if ( $triggers.length ) {
            isDialog.init( $triggers );
        } else if ( $body.length ) {
            inDialog.init( $body );
        }
    });

})( jQuery );
