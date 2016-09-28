/*
    deps: Sortable
    see https://github.com/RubaXa/Sortable

    Required html data attributes:
    * data-sortable - initiates sortable)
    * data-row - defines a row to sort

    Optional
    * data-sort-handle - to specify a specific dragging handle
    * data-sort-placeholder - field to save position of row

    * data-delete-handle - delete button
    * data-delete-placeholder - field to check as delete
 */

( function ( $, Sort ) {

    'use strict'

    function Sortable( element ) {
        this.element = $( '[data-sortable]' )
        this.rowClass = ""
        this.row = ""
        this.sortHandle = ""
        this.sortPlaceholder = ""
        this.deleteHandle = ""
        this.deletePlaceholder = ""

        self = this
        self.init()
    }

    Sortable.prototype.init = function ( ) {

        // is there a sortable element?
        if ( self.element.size() ) {
            self.rowClass = self.element.data( 'row' );
            self.row = self.element.find( self.rowClass );

            // error handling, is there something to sort?
            if ( !self.row.size() ) {
                console.log( 'Sortable: data-to-sort not valid or empty' )
                return
            }

            // optional delete
            self.deleteHandle = self.row.find( self.element.data( 'delete-handle' ) );
            if ( self.deleteHandle.size() ) {

                self.deleteHandle.on( 'click', function ( event ) {
                    self.remove( this, self );
                });
            }

            // create a sortable list
            self.sorting();
        }
    }


    Sortable.prototype.sorting = function ( ) {
        // convert jquery element in javascript element
        let htmlElement = self.element.get(0);

        // sortable config
        var config = {
            animation: 200,
            onUpdate: function ( event ) {
                // recalc positions when sorting is updated
                self.recalc()
            }
        }

        // is there a sort handle?
        self.sortHandle = self.element.data( 'sort-handle' );
        if ( self.sortHandle != undefined ) {
            config.handle = self.sortHandle;
        }

        // init sortable
        var sortable = Sort.create( htmlElement, config );
    },


    Sortable.prototype.recalc = function () {
        var items = $( self.rowClass );

        // update positions
        items.each( function ( i, el ) {
            let element = $( el );
            let index = parseInt( items.index( element ) );

            let placeholderSelector= element.data( 'sort-placeholder' );

            // find placeholder within row if not exist check outside row
            let placeholder = element.find( placeholderSelector );
            if ( !( placeholder.size() )) {
                placeholder = $( placeholderSelector );
            }

            // is there something to save to?
            if ( placeholder.size() ) {
                placeholder.val(  index  );
            }
        });
    },


    Sortable.prototype.remove = function ( el, self ) {
        let element = $( el );
        let rule = element.closest( self.rowClass );
        let ruleWrapper = rule.parent();

        // flag for deletion if there's a placeholder
        self.deletePlaceholderClass = self.element.data( 'delete-placeholder' );
        self.deletePlaceholder = rule.find( self.deletePlaceholderClass );

        if ( self.deletePlaceholder.size() ){
            self.deletePlaceholder.prop( "checked", true );
        }

        // hide rule
        rule.addClass( 'removed' ).appendTo( ruleWrapper );

        // recalc positions
        self.recalc();
    }


    // initiate
    new Sortable()

})( jQuery, Sortable );