/*
    deps: Sortable
    see https://github.com/RubaXa/Sortable

    Required html data attributes:
    * data-row - elements which need to be dragged)

    Optional
    * data-handle - handle for draggable item
    * data-delete - to delete a row, delete -requires- placeholder
 */

var sortable = {
    element: $( '[data-sortable]' ),
    row: "",
    placeholder: "",
    handle: "",
    delete: "",

    init: function () {
        var self = this;

        if ( self.element.size() ) {

            // get required data
            self.rowClass = self.element.data( 'row' );
            self.row = self.element.find( self.rowClass );
            self.placeholder = self.element.data( 'placeholder' );
            self.handle = self.element.data( 'handle' );
            self.delete = self.element.data( 'delete' );
            self.delete = self.row.find( self.delete );

            // error handling
            if ( !self.row.size() ) {
                console.log( 'Sortable: data-to-sort not valid or empty' )
                return
            }

            // optional delete, which requires placeholder
            if ( self.delete.size() && self.placeholder.size()) {

                self.delete.on( 'click', function ( event ) {
                    self.remove( this, self );
                });
            }

            // create a sortable list
            self.sorting();
        };
    },


    sorting: function () {
        var self = this

        // convert jquery element in javascript element
        let htmlElement = self.element.get(0);

        // sortable config
        var config = {
            animation: 200,
            onUpdate: function ( event ) {
                self.recalc()
            }
        }

        // is there a handle?
        if ( self.handle != undefined ) {
            config.handle = self.handle;
        }

        // init sortable
        var sortable = Sortable.create( htmlElement, config );
    },


    recalc: function () {
        var self = this;
        var items = $( self.rowClass );

        items.each( function ( i, el ) {
            let element = $( el );
            let index = parseInt( items.index( element ) );
            let placeholder = element.find( self.placeholder );

            // update placeholders with new positions
            placeholder.val(  index  );
        });
    },


    remove: function ( el, self ) {
        let element = $( el );
        let rule = element.closest( '.rule' );
        let ruleWrapper = rule.parent();

        // flag for deletion
        rule.find( '.delete input' ).prop( "checked", true );

        // hide rule
        rule.addClass( 'removed' ).appendTo( ruleWrapper );

        // recalc positions
        self.recalc();
    }
}

sortable.init()