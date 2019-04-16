// convert date format specification from the django/php syntax to the js
// datepicker spec
function django2datepicker(django_format) {
    var translation_dict = {
        '%': '',
        'y': 'yy',
        'Y': 'yyyy',
        'm': 'mm',
        'd': 'dd',
        'H': 'hh',
        'I': 'hh',
        'M': 'ii',
        'p': 'aa',
        'S': ''
    }

    var datepicker_format = '';
    for (var i = 0, len = django_format.length; i < len; i++) {
        if (django_format[i] in translation_dict) {
            datepicker_format += translation_dict[django_format[i]];
        }
        else {
            datepicker_format += django_format[i];
        }
    }

    if (datepicker_format.slice(-1) == ':') {
        datepicker_format = datepicker_format.slice(0, -1);
    }
    return datepicker_format;
}

function datetimeformatter(django_date, format) {
    var date_valid = moment(django_date, format).isValid();
    if (!date_valid) {
        return null;
    } else {
        return moment(django_date, format).toDate();
    }
}

datetime_picker_settings.dateFormat = django2datepicker(datetime_picker_settings.dateFormat);
datetime_picker_settings.timeFormat = django2datepicker(datetime_picker_settings.timeFormat);
$.fn.datepicker.language['en'] = datetime_picker_settings;


function startDatepicker() {
    $('[js-datepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-date"), $(this).attr('format') ? $(this).attr('format') : datetime_picker_settings.dateFormat);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            todayButton: true,
            language: 'en',
            startDate: date,
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })

        }).data('datepicker').selectDate(date);
    });
}

function startTimePicker() {
    $('[js-timepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-date"), $(this).attr('format') ? $(this).attr('format') : datetime_picker_settings.timeFormat);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            onlyTimepicker: true,
            language: 'en',
            startDate: date,
            timepicker: true,
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })
        }).data('datepicker').selectDate(date);
    });
}

function startDateTimePicker() {
    $('[js-datetimepicker]').each(function(index) {
        var date = datetimeformatter($(this).attr("data-datetime"),  $(this).attr('format') ? $(this).attr('format') : `${datetime_picker_settings.dateFormat} ${datetime_picker_settings.timeFormat}`);
        var instance = this;
        $(instance).attr('type', 'text');
        $(instance).datepicker({
            language: 'en',
            todayButton: true,
            startDate: date,
            timepicker: true,
            onShow: (function(inst, animationCompleted) {
                if ($(instance).val() == '') {
                    $(instance).val(' ');
                }
                return inst;
            }),
            onHide: (function(inst, animationCompleted) {
                if ($(instance).val() == ' ') {
                    $(instance).val('');
                }
                return inst;
            })
       }).data('datepicker').selectDate(date);
    });
}

function startAllPickers() {
    startDatepicker();
    startTimePicker();
    startDateTimePicker();
}
