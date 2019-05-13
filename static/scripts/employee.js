$(document).ready(
    function () {
        var form = $('#employee_edit_form');
        //console.log(form);
        //console.log($('#id_employee_office_id').val());

        var region_id = $('#id_employee_region_id');
        var employee_office_id = $('#id_employee_office_id').val();
        var employee_position_id = $('#id_employee_position_id').val();

        var office_id_val = employee_office_id.value;

        if (undefined !== region_id.val()) {
            if (region_id.val().length == 0) {
                $('#id_employee_office_id').empty();
                $('#id_employee_position_id').empty();
            } else {
                update_office_by_region(region_id,employee_office_id);
                update_position_by_region(region_id,employee_position_id);

                //$('#id_employee_office_id').val(employee_office_id);


                //console.log(employee_office_id);
                //console.log(employee_position_id);
            }
        }


        region_id.on('change', function (e) {
            //e.preventDefault();
            //console.log(region_id.val());
            if (region_id.val().length > 0) {
                update_office_by_region(region_id,employee_office_id);
                update_position_by_region(region_id,employee_position_id);
            } else {
                $('#id_employee_office_id').empty();
                $('#id_employee_position_id').empty();
            }
        })
    })

function update_office_by_region(region_id,employee_office_id) {
    $.ajax({
        url: 'update_office_by_region/',
        data: {
            'region_id': region_id.val(),
        },
        success: function (response) {
            var new_options = response;
            //console.log(new_options);
            //alert(new_options[0].office_name);  // works
            $('#id_employee_office_id').empty();
            $.each(new_options, function (key, value) {
                $('#id_employee_office_id').append($('<option>', {
                    value: value.office_id
                }).text(value.office_name));
            });
            $('#id_employee_office_id').val(employee_office_id);
        }
    });
}

function update_position_by_region(region_id,employee_position_id) {
    $.ajax({
        url: 'update_position_by_region',
        data: {
            'region_id': region_id.val(),
        },
        success: function (response) {
            var new_options = response;
            //console.log(new_options);
            $('#id_employee_position_id').empty();
            $.each(new_options, function (key, value) {
                $('#id_employee_position_id').append($('<option>', {
                    value: value.position_id
                }).text(value.position_department_id__department_name + " | " + value.position_name));
            });
            $('#id_employee_position_id').val(employee_position_id);
        }
    });
}