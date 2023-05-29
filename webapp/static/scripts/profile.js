// Function creates visited destinations graph
function createVisitedDestinationsGraph() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".profile__graph-line")

    // Get graph lines numbers
    const graphLinesNumbers = document.querySelectorAll(".profile__graph-number")

    // Define visited destinations per year array
    const visitedDestinationsPerYears = []

    // Extract per-year attribute values (i.e. visited destinations per year)
    graphLines.forEach(graphLine => {
        visitedDestinationsPerYears.push(graphLine.getAttribute("per-year"))
        graphLine.removeAttribute("per-year")
     });

    // Set specific heights and colors for graph lines
    for (let index = 0; index < visitedDestinationsPerYears.length; index++)
    {
        // Convert visited destinations per year from string to int
        visitedDestinationsPerYears[index] = parseInt(visitedDestinationsPerYears[index])
        if (! visitedDestinationsPerYears[index]) {
            // height
            graphLines[index].style.height = "5%"
            // color - default
        }
        else {
            // height grow coefficient
            height_coefficient = 95/35
            // height
            const height = 5 + height_coefficient * visitedDestinationsPerYears[index]
            graphLines[index].style.height = height.toString() + "%"
            // color
            graphLines[index].classList.add("contains")
            graphLinesNumbers[index].classList.add("contains")
        }
    }
}


// Function styles disabled upload photo button
function styleDisabledButton(button) {
    if (! button.classList.contains("disabled")) {
        button.classList.add("disabled")
    }
}

// Function styles enabled upload photo button
function styleEnabledButton(button) {
    if (button.classList.contains("disabled")) {
        button.classList.remove("disabled")
    }
}

// Function displays photo error message accordingly
function displayErrorMessage(errorMessage, errorType) {
    // Display error
    if (! errorMessage.classList.contains("active")) {
        errorMessage.classList.add("active")
    }
    // Display appropriate message for error
    if (errorType == 1) {
        errorMessage.textContent = "You don't have a selected photo anymore. Please choose one!"
    }
    if (errorType == 2) {
        errorMessage.textContent = "The selected photo does not have a valid extension. Please choose a file with a valid image extension!"
    }
    if (errorType == 3) {
        errorMessage.textContent = "The selected photo exceeds the file size limit. Please choose a smaller photo!"
    }
    if (errorType == 4) {
        errorMessage.textContent = "Please select only one photo for upload!"
    }
    // Change message color
    errorMessage.style.color = "var(--light-pink)"
}

// Function displays photo no error message
function displayNoErrorMessage(noErrorMessage){
    // Display message
    if (! noErrorMessage.classList.contains("active")) {
        noErrorMessage.classList.add("active")
    }
    // Display appropriate message in case of no error and change message color
    noErrorMessage.textContent = "Your photo is ready for upload."
    noErrorMessage.style.color = "var(--green)"

}

function getFileExtension(fileName) {
    return fileName.slice(fileName.lastIndexOf("."))
}

// Function validates photo uploading
function photoUploadValidations() {
    // Get add photo input element
    const inputPhoto = document.getElementById("upload-file-button")
    
    // Get add photo label element
    const addPhoto = document.querySelector(".profile__add-photo-button")

    // Get add photo error message element
    const infoMessagePhoto = document.querySelector(".profile__add-photo-info")

    // Get upload photo button
    const uploadPhoto = document.querySelector(".profile__upload-photo-button")
    // By default, upload photo button is disabled
    uploadPhoto.disabled =  true;

    // Add event listener for input element
    inputPhoto.addEventListener("change", function() {

        // Case: no photo chosen
        if (inputPhoto.files.length <= 0) {
            uploadPhoto.disabled =  true;
            styleDisabledButton(uploadPhoto)
            displayErrorMessage(infoMessagePhoto, 1)
        }
        // Case: one or more photo chosen
        else {
            // Case: only one photo chosen
            if (inputPhoto.files.length == 1) {
                // Get input file
                const photo = inputPhoto.files[0]
                
                // Get input file name
                const photoName = photo["name"]
                
                // Get input file extension
                const photoExtension = getFileExtension(photoName)

                // Array containing all the possible file extensions for photos
                const photoExtensions = [
                    '.apng', '.avif', '.bmp', '.gif', '.ico', '.cur', '.jpg', '.jpeg',
                    '.jfif', '.pjpeg', '.pjp', '.png', '.svg', '.svgz', '.tiff', '.tif','.xbm', '.webp'
                  ];
                
                // File size in KB
                const photo_size = photo.size / 1024
                // Maximum size in KB (=5MB)
                const size_limit = 5000
    
                // Check if input file satisfies the conditions:
                // 1. is smaller than maximum size
                // 2. is a photo
                if (photo_size < size_limit) {
                    if (photoExtensions.includes(photoExtension)) {
                        uploadPhoto.disabled =  false;
                        styleEnabledButton(uploadPhoto)
                        displayNoErrorMessage(infoMessagePhoto)
                    }
                    // Case: wrong photo extension
                    else {
                        uploadPhoto.disabled =  true;
                        styleDisabledButton(uploadPhoto)
                        displayErrorMessage(infoMessagePhoto, 2)
                    }
                }
                // Case: photo size too big
                else {
                    uploadPhoto.disabled =  true;
                    styleDisabledButton(uploadPhoto)
                    displayErrorMessage(infoMessagePhoto, 3)
                }
            }
            // Case: more photo chosen
            else {
                uploadPhoto.disabled =  true;
                styleDisabledButton(uploadPhoto)
                displayErrorMessage(infoMessagePhoto, 4)
            }
            
        }
    
    });
}


// Start after HTML code is rendered
window.addEventListener("load", () => {
    createVisitedDestinationsGraph()
    photoUploadValidations()
  });