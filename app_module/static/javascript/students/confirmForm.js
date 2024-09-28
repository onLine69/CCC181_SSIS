document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submit-form').addEventListener('click', function (event) {
        // Prevent the default form submission
        event.preventDefault();

        // Get the form associated with the button
        const form = this.closest('form');
        const originalStudentId = form.querySelector('#original-student-id') ? form.querySelector('#original-student-id').value : null;
        const studentId = form.querySelector('input[name="id_number"]').value;
        
        console.log("abot");
        if (originalStudentId === null) {
            swal("Processing adding student!", `Student with ID \"${studentId}\" will be added to the database if valid.`, "info").then(() => {
                form.submit();
            });
        } else {
            // Show the SweetAlert confirmation dialog
            swal({
                title: "Are you sure?",
                text: `Proceed with editing student with original ID: ${originalStudentId}?`,
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
                    swal("Student update is cancelled.");
                }
            });
        }
    });
});
