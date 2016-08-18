/*
    deps: Sortable
    see https://github.com/RubaXa/Sortable

    Required html data attributes:
    * data-to-sort - elements which need to be dragged)
    * data-to-update - elements where positions need to be saved
 */

var sortable = {
    element: $( '[data-sortable]' ),
    row: "",
    placeholder: "",
    delete: "",

    init: function () {
        var self = this;

        if ( self.element.size() ) {

            // get required data
            self.rowClass = self.element.data( 'row' );
            self.row = self.element.find( self.rowClass ); // add to vars?
            self.placeholder = self.element.data( 'placeholder' ); // add to vars?
            self.delete = self.element.data( 'delete' );
            self.delete = self.row.find( self.delete );

            // error handling
            if ( !self.row.size() ) {
                console.log( 'Sortable: data-to-sort not valid or empty' )
                return
            }

            // optional delete
            if ( self.delete.size() ) {

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