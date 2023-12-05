async function uploadData() {
    const form = document.getElementById('uploadForm');
    const formData = new FormData(form);
    const imageFileInput = document.getElementById('imageFile');
    const latitudeValue = document.getElementById('latitude').value;
    const longitudeValue = document.getElementById('longitude').value;
    const countryNameValue = document.getElementById('countryName').value;
    const localityValue = document.getElementById('locality').value;
    const addressValue = document.getElementById('address').value;
    
    formData.append('latitude', latitudeValue);
    formData.append('longitude', longitudeValue);
    formData.append('countryName', countryNameValue);
    formData.append('locality', localityValue);
    formData.append('address', addressValue);
    formData.append('image_file', imageFileInput.files[0]);
    
    try {
        const response = await fetch('https://banana-vision.onrender.com/upload-data', {
            method: 'POST',
            body: formData,
        });
     
        if (response.ok) {
            const responseData = await response.json();
            console.log('Success:', responseData);
        } else {
            const errorData = await response.json();
            console.error('Error:', errorData);
        }
    } catch (error) {
        console.error('An error occurred:', error);
    }
}
