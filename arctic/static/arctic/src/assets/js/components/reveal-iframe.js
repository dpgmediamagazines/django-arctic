
/*
    Reveal.js extends foundation reveal()

    Required html attributes:
    data-open = is unique id for dialog
    data-url = is url which need to be opened with iframe
 */


( function ( $ ) {

    'use strict';

    var module = {
        framed: undefined,


        init: function( element ) {
            var self = this;

            self.element = element;
            self.setup();

            // iniate listeners
            if ( self.framed ) {
                self.dialogListeners();
            } else if ( self.dialog && self.element.size() ) {
                self.listeners();
            } else {
                return false;
            };
            self.closeListeners();
            
        },


        // set all variables
        setup: function() {
            var self = this;

            // setup dialog with iframe listener
            if ( self.element && self.element.size() ) {
                self.location = window.location.href;
                self.id = self.element.data( 'open' );
                self.dialog = $( '#' + self.id );

                // dialog arguments
                self.url = self.element.data( 'url' );
                self.size = self.element.data( 'size' );
            }

            // script is loaded within an iframe
            if ( window.parent != window ) {
                self.framed = true;
                self.autoClose = self.element.data( 'auto-close' );
                self.parentReload = $('body').data( 'refresh-parent' );
            }
        },


        // listeners from within dialogs iframe
        dialogListeners: function() {
            var self = this;

            // auto close from within iframe
            if ( self.parentReload ) {
                window.parent.location.reload();
            };

            // auto close from parent
            if ( self.autoClose ) {
                self.close();
            };

            // close on click
            $( '[data-close]' ).on( 'click' , function (e) {
                e.preventDefault();
                var label = $(this).attr('aria-label') || '';
                if (label.indexOf('Dismiss') >=0) {
                    return;
                }
                self.close();
            }); 
        },
        
        //listen for the foundation close event (background click) 
        closeListeners: function() {
            
            var self = this;
            var dialog = window.parent.$( window.parent.document ).find( '.reveal' );
            
            //listen to foundation close event
            dialog.on( 'closed.zf.reveal', function () {
                self.onClose(dialog);
            });
        },

        listeners: function() {
            var self = this;
            
            // when element clicked opend dialog
            self.element.on( 'click', function ( event ) {
                event.preventDefault();

                // add sizing class
                if ( self.size ) {
                    self.dialog.addClass( self.size );
                }

                // open dialog
                self.open( self.dialog, self.url );
            })
        },

        // Manually opens dialog
        open: function( dialog, url ) {
            // listsen to foundation event to open dialog
            dialog.on( 'open.zf.reveal', function () {
                
                var iframe = dialog.find( 'iframe' );

                // setup correct url
                iframe.attr( 'src', url );

                // setup iframe height
                iframe.on( 'load' , function( ) {
                    var offset = 200;
                    var height = window.innerHeight;

                    this.style.height = height - offset + 'px';
                })
            });

            dialog.foundation( 'open' );
        },


        // closes from the cross icon inside the frame
        close: function( ) {
            var self = this;
            var dialog;

            if ( window.parent === window ) {
                dialog = $( 'body' ).find( '.reveal' );
            } else {
                dialog = window.parent.$( window.parent.document ).find( '.reveal' );
            }
            // triggers an close event to all dialogs
            dialog.foundation( 'close' );
            self.onClose(dialog);
        },
        
        // ensures the closing is done correctly, no matter if its from fundation or manually trigered 
        onClose: function(dialog) {
            // get dialog iframe
            var iframe = dialog.find( 'iframe' );
            var src = iframe.attr('src');
            var form;

            // disable areYouSure in iframe before removing src
            form = iframe.contents().find( '.dirty-check' );
            form.removeClass( 'dirty' );
            form.areYouSure( { 'silent':true } );

            // refresh the iframe
            iframe.attr( 'src', '' );
            iframe.attr( 'src', src );
        }
    }


    // iniate revealIframe
    var element = $( '[data-open][data-url], [data-open][data-auto-close]' );
    module.init( element );


    // open() and close() as global
    window.arctic.utils.revealIframe = {
        open: function( url, dialog ) {
            module.open( url, dialog );
        },
        close: function() {
            module.close();
        }
    }


})( jQuery );
0
