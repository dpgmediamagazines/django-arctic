/*
    TODO:

    - dialog with symbolic links
        = ajax ? iframe
            => refresh page na submit ( zelfde tree state (open folders)? )

    - dialog with create new
        = ajax ? iframe
            => refresh page na submit ( zelfde tree state (open folders)? )

    - http://localhost:8000/categories/create-symbolic/
        - target with search filter

    - keep state on refresh

    - sub menu in contextmenu

 */

( function ( $ ) {

    'use strict'

    function tree( element ) {
        this.element = $( '[data-tree]' );
        this.url = {};
        this.url.data = this.element.data( 'tree' );
        this.url.post = '/categories/navigation-move-node/';
        this.tree = this.element.find( '[data-tree-container]' );
        this.search = this.element.find( '[data-tree-search]' );

        // this.symbolicDialog = this.element.find( '[data-symbolic]' );
        this.symbolicDialog = $( '[data-symbolic]' );

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

        // jstree config
        self.config();

        // creates jstree
        self.build();

        // iniate search if plugin is enabled
        if ( $.inArray('search', self.plugins ) ) {
            this.search.submit( function( event ) {
                self.searchInTree( event );
            });
        }

        // handle dragged item
        self.tree.on("move_node.jstree", function ( event, data ) {
            self.isDragged( event, data )
        } );

        // interaction with tree
        // self.tree.on("changed.jstree", function ( event, data ) {
        //     console.log( data )
        //     console.log( data.changed.selected );
        //     console.log( data.changed.deselected );
        // })
    }


    // build tree config, return it and place it within self.plugins
    tree.prototype.config = function ( ) {
        var self = this;

        self.setDnd();
        self.setTypes();
        self.setContextmenu();

        // active changed
        self.plugins.push( 'changed' );

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

        var links = {
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
        }

        // handlers
        self.contextmenu = {
            "items": function ($node) {
                return links
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
                        console.log( node );

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

        // TODO POSITION CHECK!
        // show a loader..

        var postdata = {}
        postdata.parent = data.parent;
        postdata.move = data.node.id;
        postdata.position = ( data.position );

        var post = $.ajax({
            type: "POST",
            url: self.url.post,
            data: postdata,
            dataType: 'json'
        });

        post.success( function() {
            // remove loader...
        });

        post.fail( function() {
            alert( 'Error when sending drag change');
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


    // create symbolic
    tree.prototype.createSymbolic = function () {
        var self = this;

        // open dialog
        self.symbolicDialog.foundation( "open" );
    }


    // initiate
    $( function () {
        new tree();
    });


})( jQuery );