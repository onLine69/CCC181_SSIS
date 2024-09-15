document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.delete-item').forEach(button => {
    button.addEventListener('click', function (event) {
      // Prevent the default form submission
      event.preventDefault();

      // Get the form associated with the button
      const form = this.closest('form');
      const student_id = button.getAttribute('data-id');

      // Show the SweetAlert confirmation dialog
      swal({
        title: "Are you sure?",
        text: `Once deleted, you will not be able to recover the student with ID: ${student_id}!`,
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
          if (willDelete) {
            // If confirmed, submit the form
            swal(`Record of student ${student_id} has been deleted.`, {
              icon: "success",
            }).then(() => {
              form.submit();
            });
          } else {
            // If canceled, show a safe message
            swal("Student deletion is cancelled.");
          }
        });
    });
  });
});