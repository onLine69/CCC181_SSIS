document.getElementById('add-item').addEventListener('click', function () {
    var url = this.getAttribute('data-url');
    window.location.href = url;
  });