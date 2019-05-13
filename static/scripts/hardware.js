$(document).ready(function () {
    var form = $('#hardware_edit_form');
    //console.log(form);

    var region_id = $('#id_whard_region_id');
    var whard_office_id = $('#id_whard_office_id');
    var whard_mol_employee_id = $('#id_whard_mol_employee_id');
    //console.log(region_id.val());
    //console.log(whard_office_id.val());
    //console.log(whard_mol_employee_id.val());

    if (undefined !== region_id.val()) {
        if (region_id.val().length == 0) {
            $('#id_whard_office_id').empty();
            $('#id_whard_mol_employee_id').empty();
        }
    }


    region_id.on('change', function (e) {
        //e.preventDefault();
        console.log(region_id.val());
        if (region_id.val().length > 0) {
            update_office_by_region(region_id);
            update_mol_by_region(region_id);
        } else {
            $('#id_whard_office_id').empty();
            $('#id_whard_mol_employee_id').empty();
        }
    })
})

function update_office_by_region(region_id) {
    $.ajax({
        url: 'update_office_by_region/',
        data: {
            'region_id': region_id.val(),
        },
        success: function (response) {
            var new_options = response;
            //console.log(new_options);
            //alert(new_options[0].office_name);  // works
            $('#id_whard_office_id').empty();
            $.each(new_options, function (key, value) {
                $('#id_whard_office_id').append($('<option>', {
                    value: value.office_id
                }).text(value.office_name));
            });
        }
    });
}

function update_mol_by_region(region_id) {
    $.ajax({
        url: 'update_mol_by_region',
        data: {
            'region_id': region_id.val(),
        },
        success: function (response) {
            var new_options = response;
            $('#id_whard_mol_employee_id').empty();
            $.each(new_options, function (key, value) {
                $('#id_whard_mol_employee_id').append($('<option>', {
                    value: value.employee_id
                }).text(value.employee_full_fio));
            });
        }
    });
}