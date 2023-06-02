/* CONTENT LOADS / STYLES DINAMICALLY */

// Function finds the section containing a class named "active"
function findActiveSection(sections) {
    const targetClassName = "active"
    let activeSection = ""
    sections.forEach(section => {
        if (section.className.includes(targetClassName)) {
            activeSection = section
        }
    });
    return activeSection
}

// Function removes class named "active" for a section
function removeActiveSection(section) {
    section.classList.remove("active")
}

// Function adds class named "active" for a section
function addActiveSection(section) {
    section.classList.add("active")
}

// Function finds the header option containing a class named "active"
function findActiveOption() {
    let activeOption = document.querySelector(".destination__option.active")
    return activeOption
}

// Function removes class named "active" for a header option if exists one
function removeActiveOption(option) {
    if (option) {
        option.classList.remove("active")
    }
}

// Function adds class named "active" for a header option if a header option was clicked
function addActiveOption(option) {
    option.classList.add("active")
}


// Function starts when an option is clicked
function displayOptionAndSection(option, sections) {
    // For sections
    const activeSection = findActiveSection(sections)
    removeActiveSection(activeSection)
    sections.forEach(section => {
        if (section.classList[1] === option.classList[1]){
            wantedSection = section
        }
    });
    addActiveSection(wantedSection)

    // For options
    const activeOption = findActiveOption()
    removeActiveOption(activeOption)
    addActiveOption(option)
}


// Function creates average grades graph
function createGradesGraph() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".statistics__line")

    // Define average grade per field array
    const gradePerField = []

    // Extract per-year attribute values (i.e. visited destinations per year)
    graphLines.forEach(graphLine => {
        gradePerField.push(graphLine.getAttribute("grade"))
        graphLine.removeAttribute("grade")
     });

    // Set specific heights and colors for graph lines
    for (let index = 0; index < gradePerField.length; index++)
    {
        // Convert visited destinations per year from string to int
        gradePerField[index] = parseInt(gradePerField[index])

        // Case: no evaluations yet
        if (gradePerField[index] == 0) {
            graphLines[index].style.height = "5%"
            graphLines[index].classList.add("empty")
        }
        else {
            // Compute height
            height_computed = gradePerField[index] * 8

            // Set height
            graphLines[index].style.height = height_computed.toString() + "%"

            // Set color after grade
            if (gradePerField[index] < 5) {
                graphLines[index].classList.add("bad")
            }
            if (gradePerField[index] >= 5 && gradePerField[index] < 10) {
                graphLines[index].classList.add("good")
            }
            if (gradePerField[index] == 10) {
                graphLines[index].classList.add("perfect")
            }
        }
    }
}


// Function sets different colors for profile pictures of the users
// which do not have one
function setProfilePictureColors() {
    const profilePicturesLike = document.querySelectorAll(".profile__photo-like")

    // Check if there are profile pictures like and proceed accrodingly
    if (profilePicturesLike.length > 0) {
        profilePicturesLike.forEach(profilePictureLike => {
            // Randomize
            let colorOption = Math.floor(Math.random() * 5)
            // Set color
            if ([0, 1].includes(colorOption)) {
                profilePictureLike.classList.add("one")
            }
            if (colorOption == 2) {
                profilePictureLike.classList.add("two")
            }
            if ([3, 4].includes(colorOption)) {
                profilePictureLike.classList.add("three")
            }
        });
    }
}


// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get destination options
    const destinationOptions = document.querySelectorAll(".destination__option")

    // Get destination sections
    const sections = document.querySelectorAll(".section")

    // Add an event listener for every header option
    destinationOptions.forEach(option => {
            option.addEventListener("click", () => displayOptionAndSection(option, sections))
        });

    createGradesGraph()
    setProfilePictureColors()
  });