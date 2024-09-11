// Get the select element
var selectElement = document.getElementById('column-search');
var selectedValue = selectElement.getAttribute('data-selected-value');

// Set the selected option based on the value
for (var i = 0; i < selectElement.options.length; i++) {
  if (selectElement.options[i].value === selectedValue) {
    selectElement.options[i].selected = true;
    break;
  }
}