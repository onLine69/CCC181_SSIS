document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submit-form').addEventListener('click', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the form associated with the button
        const form = this.closest('form');
        const originalProgramCode = form.querySelector('#original-program-code') ? form.querySelector('#original-program-code').value : null;
        const programCode = form.querySelector('input[name="program_code"]').value;

        if (originalProgramCode === null) {
            swal("Processing adding program!", `Program with code \"${programCode}\" will be added to the database if valid.`, "info").then(() => {
                form.submit();
            });
        } else {
            // Show the SweetAlert confirmation dialog
            swal({
                title: "Are you sure?",
                text: `Proceed with editing program with original code: ${originalProgramCode}?`,
                icon: "warning",
                buttons: true,
                dangerMode: true,
            }).then((willProceed) => {
                if (willProceed) {
                    // If confirmed, submit the form
                    swal("Processing the update.", {
                        icon: "info",
                    }).then(() => {
                        form.submit();
                    });
                } else {
                    // If canceled, show a safe message
                    swal("Program update is cancelled.");
                }
            });
        }
    });
});
