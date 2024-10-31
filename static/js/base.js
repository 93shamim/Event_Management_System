
// for all table (table row, panination, sorting, ordering, searching)

    $(document).ready(function() {
        $('.TableAttributes').DataTable({
            "paging": true,
            "ordering": true,
            "searching": true,
            "order": [[ 0, "asc" ]],
            "pageLength": 10,

        });
    });


// for user status apply(active/deactive)
    // function toggleUserStatus(userId) {
    //     $.ajax({
    //         type: 'POST',
    //         url: '{% url 'toggle_user_status' %}',
    //         data: {
    //             'user_id': userId
    //         },
    //         success: function(data) {
    //             if (data.success) {
    //                 // Update the user status in the table
    //                 $('#user-status-' + userId).text(data.status);
    //             } else {
    //                 alert('Error toggling user status');
    //             }
    //         }
    //     });
    // }