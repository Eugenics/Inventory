$(document).ready(function () {
    var form = $('#department_edit_form');
    //console.log(form);

    var region_id = $('#id_department_region_id');
    var department_parent_id = $('#id_department_parent_id').val();

    //console.log(region_id.val());
    //console.log(department_parent_id.val());

    if (undefined !== region_id.val()) {
        if (region_id.val().length == 0) {
            $('#id_department_parent_id').empty();
        } else {
            update_department_by_region(region_id, department_parent_id);
        }
    }

    region_id.on('change', function (e) {
        if (region_id.val().length > 0) {
            update_department_by_region(region_id, department_parent_id);
        } else {
            $('#id_department_parent_id').empty();
        }
    })
})

function update_department_by_region(region_id, department_parent_id) {
    $.ajax({
        url: 'update_department_by_region/',
        data: {
            'region_id': region_id.val(),
        },
        success: function (response) {
            var new_options = response;
            //console.log($('#id_department_parent_id'));
            $('#id_department_parent_id').empty();
            $("#id_department_parent_id").prepend("<option value=''></option>").val('');
            $.each(new_options, function (key, value) {
                $('#id_department_parent_id').append($('<option>', {
                    value: value.department_id
                }).text(value.department_name));
            });
            $('#id_department_parent_id').val(department_parent_id);
        }
    });
}