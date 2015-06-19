var checked_count = 0;
var last_checked_id = 0;
    // Group deletion warning
    $('#delete').submit(function() {
        return confirm("Are you sure? "+checked_count+" will be deleted!");
    });
    // Assign to each checkbox action witch control edit button state and group_id for edit form
    $('.check').each(function () {
        console.log($(this).attr('value'));
        $(this).click( function () {
            if ($(this).is(':checked')) {
                checked_count++;
                change_edit_btn_state();
                $('#g_id').attr('value', $(this).prop('value'))
                console.log($('#g_id').attr('value'))
            } else {
                checked_count--;
                change_edit_btn_state();
            }
        console.log(checked_count)
        });
    });
    // Activate edit button if only one group checked
    function change_edit_btn_state() {
        if((checked_count == 1)) {
            $('#edit_btn').prop('disabled', false);
        } else {
            $('#edit_btn').prop('disabled', true);
        }
    }