( function ( $ ) {

    function ConditionalField( element ) {

        if ( element instanceof jQuery || element.attr('id') == 'id' ) {
            this.form = element.closest( 'form' );
            this.state = 0;
            this.element = element;
            this.id = element.attr( 'id' );
            this.value = element.val();
            this.checkbox = $( '<input type="checkbox" id="' + this.id + '_toggler" />' );

            this.setup();
            this.init();

        } else {
            throw new Error ( 'Expecting a jQuery object with an ID attribute' )
        }
    }


    ConditionalField.prototype.setup = function ( ) {
        this.element.parent().addClass( 'is-conditional-field' )
        if ( this.value && this.value.length ) {
            this.state = 1
            this.checkbox = this.checkbox.attr( 'checked', 'checked' )
        } else {
            setTimeout(function(){ this.hidden(); }.bind(this), 0);
            //wait for selectize if exists
        }

        this.element.before( this.checkbox )
        this.checkbox.wrap( '<div class="input-group-label"></div>' )

        this.element.wrap( '<div class="input-group-field"></div>' )
    }


    ConditionalField.prototype.init = function ( ) {
        var self = this

        if ( this.value ) {
            this.visible()
        } else {
            this.hidden()
        }

        this.checkbox.change( function() {
            if ( this.checked ) {
                self.visible()
            } else {
                self.hidden()
            }
        })

        this.form.on( 'submit', function ( event ) {
            event.preventDefault()

            if ( self.state === 0 ) {
                self.empty( self )
            }

            this.submit();
        });
    }


    ConditionalField.prototype.hidden = function ( ) {
        this.element.parent().hide()
        this.state = 0
    }


    ConditionalField.prototype.visible = function ( ) {
        this.element.parent().show()
        this.state = 1
    }


    ConditionalField.prototype.empty = function ( self ) {
        self.element.val( "" )
    }


    $( document ).ready( function () {
        var field = $( '#id_shops' )
        new ConditionalField( field )
    });

})( jQuery )
