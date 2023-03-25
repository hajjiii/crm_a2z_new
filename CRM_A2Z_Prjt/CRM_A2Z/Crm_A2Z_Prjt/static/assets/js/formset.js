

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
    replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}
function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (formCount < 1000) {
        // Create a new row with the same structure as the previous row
        var newRow = $('<tr class="item">' + $('.item:first').html() + '</tr>');

        // Clear the form fields
        newRow.find('.formset-field').each(function () {
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });
        newRow.find('.formset-field').not(':checkbox').val('');

        // Insert the new row after the last row
        newRow.appendTo('#overflow table tbody');

        // Relabel or rename all the relevant bits
        newRow.find('.formset-field').each(function () {
            updateElementIndex(this, prefix, formCount);
        });

        // Add an event handler for the delete item/form link
        newRow.find(".delete").click(function () {
            return deleteForm(this, prefix);
        });

        // Update the total form count
        $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
    }
    return false;
}
function deleteForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount > 1) {
          // Delete the item/form
          var goto_id = $(btn).find('input').val();
          if( goto_id ){
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/"+ goto_id +"/?next="+ window.location.pathname,
                error: function () {
                  console.log("error");
                },
                success: function (data) {
                  $(btn).parents('.item').remove();                 
                },
                type: 'GET'
            });
          }else{
            $(btn).parents('.item').remove();
          }

          var forms = $('.item'); // Get all the forms
          // Update the total number of forms (1 less than before)
          $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
          var i = 0;
          // Go through the forms and set their indices, names and IDs
          for (formCount = forms.length; i < formCount; i++) {
              $(forms.get(i)).find('.formset-field').each(function () {
                  updateElementIndex(this, prefix, i);
              });
          }
      } // End if

      return false;
  }

  $("body").on('click', '.remove-form-row',function () {
    deleteForm($(this), String($('.add-form-row').attr('id')));
  });

  $("body").on('click', '.add-form-row',function () {
      return addForm($(this), String($(this).attr('id')));
  });
