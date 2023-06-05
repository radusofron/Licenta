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
    let activeOption = document.querySelector(".evaluate__option.active")
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

// Function validates whether the button can be clicked or not based on the condition that a 
// checkbox must be checked for every row. It checks the status of each checkbox and enables or 
// disables the button accordingly.
function validateEvaluation() {
    // Get button
    const button = document.querySelector(".evaluate__button")
    
    // Get all the rows
    const rows = document.querySelectorAll(".evaluate__grade-container")
    
    // For every row, check if a checkbox is checked
    for (const row of rows) {
        // Get checkboxes
        const checkboxes = row.querySelectorAll('input[type="checkbox"]')
        let isChecked = false
        for (const checkbox of checkboxes) {
            if (checkbox.checked) {
                isChecked = true
            }
        }
        // If no checkbox is checked on a row, exit function
        if (isChecked == false) {
            if (button.disabled == false) {
                button.disabled = true
                styleDisabledButton(button)
            }
            return
        }
    }

    // Case: all the rows have a checkbox checked
    // Enable button
    button.disabled = false;
    styleEnabledButton(button)
}

// Function updates checkboxes' status by unchecking the current checkbox if a new one is checked
function changeCheckboxesStatus(checkboxes) {

    // Enable single selection for checkboxes: uncheck others when one is checked
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener("change", function() {
            // If new checkbox is checked, then uncheck the others
            if (checkbox.checked) {
                checkboxes.forEach(otherCheckbox => {
                    if (checkbox !== otherCheckbox) {
                        otherCheckbox.checked = false
                    }
                });
            }
            validateEvaluation()
        });
    });
}

// Function extracts all the checkboxes for every row in the table
function getCheckboxes() {
    // Checkboxes names
    const names = ["Attractions", "Accomodation", "Culture", "Entertainment", "Food and drink", 
    "History", "Natural beauty", "Night life", "Transport", "Safety"]
    // For every row, get checkboxes
    for (let index = 0; index < 10; index++) {
        let checkboxes = document.getElementsByName(names[index])
        changeCheckboxesStatus(checkboxes)
    }
}


// Function applies a specific style to the sticky element when it reaches the top of the page.
function setStyletToStickyElement () {
    // Get sticky element
    const stickyElement = document.querySelector(".evaluate__middle-container")

    let isAtTheTop = false

    // Change style if window was scrolled
    document.addEventListener("scroll", () => {
        // Get sticky element position
        positions = stickyElement.getBoundingClientRect()
        
        // When sticky element is at the top, apply style
        if (positions.top == 0) {
            if (isAtTheTop == false) {
                stickyElement.style.boxShadow = "0rem 0.25rem 1rem #7EBDC2"
                isAtTheTop = true
            }
        }
        // Else remove style
        else {
            if (isAtTheTop == true) {
                stickyElement.style.boxShadow = ""
                isAtTheTop = false
            }
        }
    });
}


// Function to display the remaining characters for the user's review
function displayCharactersLeft() {
    // Set maximum length
    const maxLength = 512

    // Get input element
    const reviewInput = document.querySelector(".review__input")

    // Get element for display
    const charactersRemaining = document.querySelector(".review__input-remaining")

    // Add an event listener for input element
    reviewInput.addEventListener("input", function() {
        // Extract text review
        const review = reviewInput.value

        // Case: nothing found
        if (review === "") {
             charactersRemaining.innerHTML = "Characters left: 512"
        }
        // Case: user writes
        else {
            // Calculate the difference
            const diff = maxLength - review.length

            // Change color when no character remained
            if (diff == 0) {
                charactersRemaining.style.color = "#D47E73"
            }
            if (diff == 1) {
                charactersRemaining.style.color = "#8C98AD"
            }
            
            // Display the remaining characters
            charactersRemaining.innerHTML = "Characters left: " + diff.toString()
        }
    });
}


// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get evaluation options
    const evaluateOptions = document.querySelectorAll(".evaluate__option")

    // Get evaluation sections
    const sections = document.querySelectorAll(".section")

    // Add an event listener for every header option
    evaluateOptions.forEach(option => {
            option.addEventListener("click", () => displayOptionAndSection(option, sections))
        });

    getCheckboxes()
    setStyletToStickyElement()
    displayCharactersLeft()
  });