( function ( $ ) {

    var setCsrf = {
        token: arctic.utils.getCookie('csrftoken'),

        init: function () {
            this.ajaxSetup()
        },

        csrfSafeMethod: function (method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        },

        ajaxSetup: function () {
            var self = this;

            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if ( !self.csrfSafeMethod( settings.type ) && !this.crossDomain ) {
                        xhr.setRequestHeader( "X-CSRFToken", self.token );
                    }
                }
            });
        }
    };

    setCsrf.init();

})( jQuery )