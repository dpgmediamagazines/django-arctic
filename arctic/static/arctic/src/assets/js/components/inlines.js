function startDynamicInlines() {
    let inlineFormSelector = '[data-inline-form]';
    hideFields(inlineFormSelector);
    deleteButton(inlineFormSelector);
    checkMaxNum(inlineFormSelector);

    $('[js-data-inline-button]').off().on('click', function(e){
        e.preventDefault();
        let max_num = this.getAttribute('data-inline-max-num');
        let $parent = $(this).parent();
        let $inlineForm = $parent.find(inlineFormSelector);
        inlineForm = $inlineForm[$inlineForm.length -1];
        selectizes = checkSelectizes();
        let $clonedInline = $(inlineForm).clone().removeClass('hide');

        // Change all the atributes in the hidden for for the next inline
        let $nameSet = $(inlineForm).find('input[name*="_set-"]');
        let $idSet = $(inlineForm).find('input[id*="_set-"]');
        let $forSet = $(inlineForm).find('[for*="_set-"]');
        let setNameArray = $nameSet[0].getAttribute('name').split('_');
        let setName = setNameArray[0];

        // find total number and increment
        let $totalForm = $('input[name=' + setName + '_set-TOTAL_FORMS]');
        let number = $totalForm.val();

        // Find all id, names and for fields and replace the content with a +1 increment
        changeFields($nameSet, 'name', number);
        changeFields($idSet, 'id', number);
        changeFields($forSet, 'for', number);
        $totalForm.val(parseInt(number) + 1);
        $(inlineForm).prev().append($clonedInline);
        if (selectizes) {
            startAllSelectizes();
        }
        deleteButton(inlineFormSelector);
        startAllPickers();
        startSortInlines();
        floatLabels();
        betterFile();

        // check max number
        if (max_num == $inlineForm.length) {
            $(this).hide();
        }
    });

    function deleteButton(inlineFormSelector) {
        //Hide all delete checkboxes and bind the button
        let deleteButtonSelector = '[js-inline-delete]';
        let deleteInput = 'input[name*="DELETE"]';
        $(deleteButtonSelector).off().on('click', function() {
            $parent = $(this).closest(inlineFormSelector);
            $deleteCheckbox = $parent.find(deleteInput);
            $deleteCheckbox[0].checked = true;
            $parent.addClass('hide');
        });
    }

    function changeFields($set, type, number) {
        let currentNumberAttr = '-' + (number - 1) +'-';
        let newNumberAttr = '-' + number +'-';
        for(let i=0, len = $set.length; i < len; i++) {
            item = $set[i];
            attribute = item.getAttribute(type);
            attribute = attribute.replace(currentNumberAttr, newNumberAttr);
            item.setAttribute(type, attribute);
        }
    }

    function checkSelectizes() {
        $selectize = $(inlineForm).find('[js-selectize-multiple], [js-selectize-autocomplete], [js-selectize]');
        if ($selectize.length) {
            for(let i=0, len = $selectize.length; i < len; i++) {
                let selectize = $selectize[i];
                if (selectize.selectize) {
                    let value = $(selectize).val();
                    selectize.selectize.destroy();
                    $(selectize).val(value);
                }
            }
            return true
        }
        return false
    }

    function hideFields(inlineFormSelector) {
        // hides delete
        let deleteInput = 'input[name*="DELETE"]';
        let $delete$Fields = $(inlineFormSelector).find(deleteInput);
        $delete$Fields.closest('.row').addClass('hide');
    }

    function checkMaxNum(inlineFormSelector) {
        // Check if the form already reached the max number of fields
        let $addButton = $('[js-data-inline-button]');
        for(let i = 0, len = $addButton.length; i < len; i++) {
            let button = $addButton[i];
            let $parent = $(button).parent();
            let $inlineForm = $parent.find(inlineFormSelector);
            let max_num = button.getAttribute('data-inline-max-num');
            if (max_num == $inlineForm.length) {
                $(button).hide();
            }
        }
    }
 }

 function checkOrder(fields) {
     if (fields.length) {
         for(let i=0, len = fields.length; i < len; i++) {
             field = fields[i];
             field.value = i;
         }
     }
 }

 function startSortInlines() {
     // check if sort is enebale if so set the order on init
     $('[data-sorting-field]').each(function(index) {
         // Hide order field
         let orderFieldName = this.getAttribute('data-sorting-field');
         let orderInput = 'input[name*="-' + orderFieldName + '"]';
         let orderFields = this.querySelectorAll(orderInput);
         $(orderFields).closest('.row').addClass('hide');

         checkOrder(orderFields);

         Sortable.create(this, {
             handle: '.inline-form-grab',
             onUpdate: function (e) {
                 let el = e.item.parentElement;
                 let orderFieldName = el.getAttribute('data-sort-field');
                 let orderInput = 'input[name*="-' + orderFieldName + '"]';
                 let orderFields = el.querySelectorAll('input[name*="-order"]');
                 checkOrder(orderFields);
             }
         });
     });
 }

function startAllInlines() {
    startDynamicInlines();
    startSortInlines();
}
