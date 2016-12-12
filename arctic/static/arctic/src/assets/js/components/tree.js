/*
    TODO:
    - http://localhost:8000/categories/create-symbolic/
        - target with search filter
    - keep state on refresh
 */

( function ( $ ) {

    'use strict'

    function tree( element ) {
        this.element = $( '[data-tree]' );
        this.tree = this.element.find( '[data-tree-container]' );
        this.search = this.element.find( '[data-tree-search]' );

        this.url = {};
        this.url.data = this.element.data( 'tree' );
        this.url.category_move = '/categories/navigation-move-node/';
        this.url.category_create = '/categories/create/#';
        this.url.symbolic_create = '/categories/symbolic/create/#/?dialog=true';
        this.url.category_detail = '/categories/#/';
        this.url.symbolic_detail = '/categories/symbolic/#/';

        this.plugins = [];

        var self = this;
        self.init();
    }


    tree.prototype.init = function ( ) {
        var self = this;

        // jstree config
        self.config();

        // creates jstree
        self.build();

        // iniate search if plugin is enabled
        if ( $.inArray( 'search', self.plugins ) ) {
            this.search.submit( function( event ) {
                self.searchInTree( event );
            });
        }

        // handle dragged item
        self.tree.on("move_node.jstree", function ( event, data ) {
            self.isDragged( event, data )
        } );
    }


    // build tree config, return it and place it within self.plugins
    tree.prototype.config = function ( ) {
        var self = this;

        self.setDnd();
        self.setTypes();
        self.setContextmenu();

        // active changed
        // self.plugins.push( 'changed' );

        // whole row
        self.plugins.push( 'wholerow' );

        // activate search when <data-tree-search /> is set
        if ( self.search.length ) {
            self.plugins.push( 'search' );
        }
    }


    // drag and drop
    tree.prototype.setDnd = function ( ) {
        var self = this;

        // activate plugin
        self.plugins.push( 'dnd' );

        // callbacks
        self.dnd_callback = {
            drop_check: function ( data ) {
                console.log( data, 'checked')
            }
        }
    }


    // types and add icons
    tree.prototype.setTypes = function ( ) {
        var self = this;

        // activate plugin
        self.plugins.push( 'types' );

        // set types
        self.types = {};
        self.types.symbolic = {
            "icon": "symbolic"
        };
    }


    // context menu
    tree.prototype.setContextmenu = function ( ) {
        var self = this;

        // activate plugin
        self.plugins.push( 'contextmenu' );

        var categoryLinks = function ( node ) {
            var items = {
                "Open": {
                    "label": "Open",
                    "action": function ( obj ) {
                        window.location = self.url.category_detail.replace( '#', node.id );
                    }
                },
                "Create": {
                    "label": "Create new",
                    "action": function ( obj ) {
                        self.createCategory( node );
                    }
                },
                "Other": {
                    "label": "Add other",
                    "submenu" :{
                        "Symbolic": {
                            "label": "Create symbolic",
                            "action": function ( obj ) {
                                self.createSymbolic( node );
                            }
                        }
                    }
                }
            }

            return items;
        }


        var symbolicLinks = function ( node ) {

            var items = {
                "Open": {
                    "label": "Open",
                    "action": function ( obj ) {
                        window.location = self.url.symbolic_detail.replace( '#', node.id );
                    }
                }
            }

            return items;
        }

        // handlers
        self.contextmenu = {
            "items": function ( node ) {

                // symbolic has own menu
                if ( node.li_attr.type == 'symboliccategory' ) {
                    return symbolicLinks( node )
                } else {
                    return categoryLinks( node )
                }
            }
        }
    }


    // builds tree
    tree.prototype.build = function ( ) {
        var self = this;

        self.tree.jstree({
             'core' : {
                'check_callback' : function (operation, node, node_parent, node_position, more) {

                    // it's a drag event
                    if ( more && more.dnd && ( operation === 'move_node' )) {

                        // disable dragging on root level
                        if ( node.parent === '#' ) {
                            return false;
                        }

                        // limit dragging to same parent level
                        if ( node.parent !== node_parent.id ) {
                            return false;
                        }

                    }

                    return true;
                },
                'data' : {
                    "url" : self.url.data,
                    "data" : function ( node ) {

                        if ( node.id == '#' ) {
                            return { "level" : 0 };
                        } else {
                            return { "id" : node.id };
                        }
                    }
                }
            },
            "plugins": self.plugins,
            "types" : self.types,
            "contextmenu": self.contextmenu,
            "dnd": self.dnd
        })
    }


    // posts new location of dragged node
    tree.prototype.isDragged = function ( event, data ) {
        var self = this;

        var loader = arctic.utils.growl( 'warning', 'Saving...', 'your latest changes to the server' );

        var postdata = {}
        postdata.parent = data.parent;
        postdata.move = data.node.id;
        postdata.position = ( data.position );

        var post = $.ajax({
            type: "POST",
            url: self.url.category_move,
            data: postdata,
            dataType: 'json'
        });

        post.success( function() {
            loader.remove();
            var notification = arctic.utils.growl( 'success', 'Saved', 'your latest changes' );
            notification.delay( 1000 ).fadeOut();
        });

        post.fail( function() {
            loader.remove();
            var notification = arctic.utils.growl( 'error', 'Error...', 'when sending drag change' );
            throw new Error( 'Error when sending drag change' );
        });
    }


    // search within tree
    tree.prototype.searchInTree = function ( event ) {
        event.preventDefault();

        var self = this;
        var searchValue = self.search.find( 'input[type=text]' ).val();

        $( '[data-tree-container]' ).jstree( true ).search( searchValue );
    }


    // open dialog with create category
    tree.prototype.createCategory = function ( node ) {
        var self = this;

        var dialog = $( '[data-reveal]' );

        if ( dialog && node.id ) {
            var url = self.url.category_create.replace( '#', node.id );
            window.location = url
        }
    }

    // open dialog with create symbolic
    tree.prototype.createSymbolic = function ( node ) {
        var self = this;

        var dialog = $( '[data-reveal]' );

        if ( dialog && node.id ) {
            var url = self.url.symbolic_create.replace( '#', node.id );

            // open dialog
            arctic.utils.revealIframe.open( dialog, url );
        }
    }


    // initiate
    $( function () {
        new tree();
    });


})( jQuery );