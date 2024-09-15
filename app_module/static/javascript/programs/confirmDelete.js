document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.delete-item').forEach(button => {
        button.addEventListener('click', function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // Get the form associated with the button
            const form = this.closest('form');
            const program_code = button.getAttribute('data-id');

            // Show the SweetAlert confirmation dialog
            swal({
                title: "Are you sure?",
                text: `Once deleted, you will not be able to recover the program with code: ${program_code}, 
                and all students enrolled will be unenrolled!`,
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willDelete) => {
                    if (willDelete) {
                        // If confirmed, submit the form
                        swal(`Record of program ${program_code} has been deleted.`, {
                            icon: "success",
                        }).then(() => {
                            form.submit();
                        });
                    } else {
                        // If canceled, show a safe message
                        swal("Program deletion is cancelled.");
                    }
                });
        });
    });
});