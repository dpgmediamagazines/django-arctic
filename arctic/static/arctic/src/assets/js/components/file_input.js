function get_file_preview(target, url, filename) {
    var img = new Image();
    img.onerror = function(evt) {
        target.html('<a href="' + url + '" download="' + filename + '">' + filename + '</a>');
        target.prev().height(target.height());
    }
    img.onload = function(evt) {
        target.html('<a href="' + this.src + '" target="_blank"><img src="' + this.src + '" /></a>');
        if (target.height() < 22) {
            setTimeout(function(){ target.prev().height(target.height()); }, 20);
        }
        else {
            target.prev().height(target.height());
        }
    }
    img.src = url;
    if ($(target).next('.better-file-clear-checkbox')) {
        $(target).next('.better-file-clear-checkbox').prop('checked', false);
        $(target).next().next().show();
    }
    return false;
}

function arcticImageEvent(eventName, eventData) {
    var arcticEvent = '';
    if(typeof(Event) === 'function') {
        //normal browsers
        arcticEvent = new CustomEvent(eventName, { detail: eventData});
    } else {
        //IE browsers
        arcticEvent = document.createEvent('Event');
        arcticEvent.detail = eventData;
        arcticEvent.initEvent(eventName, true, true);
    }
    document.dispatchEvent(arcticEvent);
}

function betterFile() {
    $('.better-file').each(function() {
        var input = $(this).find('input[type=file]');
        var label = $(this).find('label');
        var clear = $(this).find('.better-file-clear');

        $(input).off().on('change', function() {
            var url = URL.createObjectURL($(this).prop('files')[0])
            get_file_preview(label, url, $(this).prop('files')[0].name);
            var data = this;
            arcticImageEvent('arcticImageAdded', data);
        });

        if ($(input).attr('initial')) {
            var url = $(input).attr('initial');
            var filename = url.split('\\').pop().split('/').pop();
            get_file_preview(label, url, filename);
            if (clear) {
                $(clear).show();
            }
        }

        $(label).off().on('click', function() {
            if ($(this).children().first().attr('href') == '#upload') {
                $(this).prev().click();
                return false;
            }
            return true;
        });

        $(clear).off().on('click', function() {
            var checkbox = $(this).prev();
            var data = $(this).parent().parent().find('input[type=file]');
            $(checkbox).prop('checked', true);
            $(this).hide();
            $(label).html('<a href="#upload">' + $(label).attr('placeholder') + '</a>');
            $(label).prev().height(label.height());
            data.val(null); //reset input field so we can add the same image again;
            arcticImageEvent('arcticImageRemoved', data);
            return false;
        });
    });
}
