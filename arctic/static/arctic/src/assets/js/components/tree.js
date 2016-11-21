/*
    TODO:
    - symbolic icon
    - massload
    - dialog with symbolic links
        - this.data and filter symbolic links
 */

( function ( $ ) {

    'use strict'

    function tree( element ) {
        this.element = $( '[data-tree]' );
        this.data = this.element.data( 'tree' );
        this.tree = this.element.find( '[data-tree-container]' );
        this.search = this.element.find( '[data-tree-search]' );
        this.symbolicDialog = this.element.find( "#symbolic" );
        this.plugins = [];

        this.options = {};
        this.options.url = {};
        this.options.url.create = this.element.data( 'create' );

        var self = this;
        self.init();

        window.foo = this;
    }

    tree.prototype.init = function ( ) {
        var self = this;

        self.config();
        self.build();

        // iniate search if plugin is enabled
        if ( $.inArray('search', self.plugins ) ) {
            this.search.submit( function( event ) {
                self.searchTree( event );
            });
        }

        self.tree.on( 'changed.jstree' , function (e, data) {
            console.log(data.node.id);
        });
    }

    // build tree config, return it and place it within self.plugins
    tree.prototype.config = function ( ) {
        var self = this;

        // activate drag and drop
        self.plugins.push( 'dnd' );

        self.plugins.push( 'changed' );

        // activate context menu
        self.plugins.push( 'contextmenu' );

        // activate search when <data-tree-search> is set
        if ( self.search.length ) {
            self.plugins.push( 'search' );
        }

        /*
            TODO

            activate massload for large numbers of items
            self.plugins.push( 'massload' );
        */

        // activate types and add icons
        self.plugins.push( 'types' );

        self.types = {};
        self.types.symbolic = {
            "icon": "symbolic"
        };
    }


    // buils tree
    tree.prototype.build = function ( ) {
        var self = this;

        self.tree.jstree({
            "core" : {
                "check_callback": true,
                "data" : {
                    "url" : self.data,
                    "data" : function (node) {
                        return { "id" : node.id };
                    }
                }
            },
            "plugins": self.plugins,
            "types" : self.types,
            "contextmenu": {
                "items": function ($node) {
                    return {
                        "Create": {
                            "label": "Create new",
                            "action": function ( obj ) {
                                if ( self.options.url.create ) {
                                    window.location = self.options.url.create;
                                }
                            }
                        },
                        "Symbolic": {
                            "label": "Create symbolic",
                            "action": function ( obj ) {
                                self.createSymbolic();
                            }
                        }
                    };
                }
            }
        });
    }

    // search in tree
    tree.prototype.searchTree = function ( event ) {
        var self = this;
        var searchValue = self.search.find( 'input[type=text]' ).val();

        event.preventDefault();
        $( '[data-tree-container]' ).jstree( true ).search( searchValue );
    }

    tree.prototype.createSymbolic = function () {
        console.log('create symbolic');

        // open dialog
        self.symbolicDialog.trigger( "open.zf.reveal" );
    }

    // initiate
    new tree();

})( jQuery );