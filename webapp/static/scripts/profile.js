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
        errorMessage.textContent = "The selected photo exceeds the file size limit. Please choose a smaller photo!"
    }
    if (errorType == 3) {
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
                // Get input photo
                const photo = inputPhoto.files[0]
                
                // Photo size in KB
                const photo_size = photo.size / 1024
                // Maximum size in KB (=5MB)
                const size_limit = 5000
    
                // Check if input photo satisfies the conditions
                if (photo_size < size_limit) {
                    uploadPhoto.disabled =  false;
                    styleEnabledButton(uploadPhoto)
                    displayNoErrorMessage(infoMessagePhoto)
                }
                else {
                    uploadPhoto.disabled =  true;
                    styleDisabledButton(uploadPhoto)
                    displayErrorMessage(infoMessagePhoto, 2)
                }
            }
            // Case: more photo chosen
            else {
                uploadPhoto.disabled =  true;
                styleDisabledButton(uploadPhoto)
                displayErrorMessage(infoMessagePhoto, 3)
            }
            
        }
    
    });
}


// Start after HTML code is rendered
window.addEventListener("load", () => {
    createVisitedDestinationsGraph()
    photoUploadValidations()
  });