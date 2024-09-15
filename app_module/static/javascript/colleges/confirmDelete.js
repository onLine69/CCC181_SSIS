document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // Get the form associated with the button
            const form = this.closest('form');
            const college_code = button.getAttribute('data-id');

            // Show the SweetAlert confirmation dialog
            swal({
                title: "Are you sure?",
                text: `Once deleted, you will not be able to recover the college with code: ${college_code}, all the programs under it will be deleted and all students enrolled will be unenrolled!`,
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willDelete) => {
                    if (willDelete) {
                        // If confirmed, submit the form
                        swal(`Record of college ${college_code} has been deleted.`, {
                            icon: "success",
                        }).then(() => {
                            form.submit();
                        });
                    } else {
                        // If canceled, show a safe message
                        swal("College deletion is cancelled.");
                    }
                });
        });
    });
});