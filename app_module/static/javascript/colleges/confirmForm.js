document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submit-form').addEventListener('click', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the form associated with the button
        const form = this.closest('form');
        const originalCollegeCode = form.querySelector('#original-college-code') ? form.querySelector('#original-college-code').value : null;
        const collegeCode = form.querySelector('input[name="college_code"]').value;

        if (originalCollegeCode === null) {
            swal("Processing adding college!", `college with code \"${collegeCode}\" will be added to the database if valid.`, "info").then(() => {
                form.submit();
            });
        } else {
            // Show the SweetAlert confirmation dialog
            swal({
                title: "Are you sure?",
                text: `Proceed with editing college with original code: ${originalCollegeCode}?`,
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
                    swal("College update is cancelled.");
                }
            });
        }
    });
});
