const defaultImage = document.getElementById('default-profile').value;
const originalImageSrc = document.getElementById('alt-profile').value; // Store the original image source

var file_input = document.getElementById('profile-picture');
var image_profile = document.getElementById('college-image');
var alt_path = document.getElementById('alt-profile');

function preview(size) {
    var file = file_input.files[0];
    var fileSize = (file.size / (1024 * 1024)).toFixed(2);

    // Validate file type
    if (!['image/jpg', 'image/jpeg', 'image/png'].includes(file.type)) {
        image_profile.src = originalImageSrc; // Reset image to default
        // Reset the input to force the filename to clear
        file_input.type = '';
        file_input.type = 'file';
        alert("Please select a valid image file (JPG, JPEG, or PNG).");
        return;
    }
    
    if (fileSize > size) {
        image_profile.src = originalImageSrc;
        // Reset the input to force the filename to clear
        file_input.type = '';
        file_input.type = 'file';
        alert(`File size must be less than ${size} MB.`);
        return;
    }

    image_profile.src = URL.createObjectURL(event.target.files[0]);
    alt_path.value = image_profile.src;
}

function resetPic() {
    // Clear the file input and restore the original image
    file_input.value = '';
    image_profile.src = originalImageSrc; // Restore the original image
    alt_path.value = originalImageSrc;
}

function removePic() {
    // Restore the default image and clear the file input
    file_input.value = '';
    image_profile.src = defaultImage; // Set to default image
    alt_path.value = defaultImage;
}