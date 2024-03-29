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


// Function returns touristic objectives which match the search
function returnTouristicObjectives() {
    // Get touristic objectives
    const objectives = document.querySelectorAll(".travel-itineraries__objective")

    // Get search bar input
    const inputExtracted = document.querySelector(".travel-itineraries__input").value
    // Transform input to lowercase input
    const input = inputExtracted.toLowerCase()

    // Check if input is empty; if so, display all the touristic objectives again and stop
    if (input.trim() === "") {
        objectives.forEach(objective => {
          // If destination is inactive, make it active
          if (objective.classList[1] === "inactive") {
            objective.classList.remove("inactive");
          }
        });
        return
    }

    // Variable used to know if no objective will be returned
    let minimumAnObjectiveReturned = false

    // Get element used for no results found message
    const noResultsMessage = document.querySelector(".travel-itineraries__results-not-found")

    // Search for matches
    objectives.forEach(objective => {
        // Extract touristic objective from HTML
        const objectiveName = objective["children"][0].textContent.toLowerCase()

        // Trim the strings in order to compare them
        if (objectiveName.trim() === input.trim() || objectiveName.trim().startsWith(input.trim()) || objectiveName.trim().endsWith(input.trim()) || objectiveName.trim().includes(input.trim())) {
            // If destination is inactive, make it active
            if (objective.classList[1] === "inactive"){
                objective.classList.remove("inactive");
            }
        }
        else {
        // If destination is active, make it inactive
        if (objective.classList[1] !== "inactive") {
            objective.classList.add("inactive");
        }
        }
        // Check if there is at least a destination which will be displayed (does not have "inactive" class)
        if (!objective.classList.contains("inactive")) {
            minimumAnObjectiveReturned = true
        }
    });

    // Check if no results were found in order to display appropiate message
    if (minimumAnObjectiveReturned) {
        if (noResultsMessage.classList.contains("active")) {
            noResultsMessage.classList.remove("active")
        }
    }
    else {
        if (!noResultsMessage.classList.contains("active")){
            noResultsMessage.classList.add("active")
        }
    }
}


/* TRAVEL ITINERARY */
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

// Function validates wheter the button can be clicked or not based on the following conditions:
// - number of days has to be selected
// - number of tourisitc objectives has to be at least equal with the number of days selected
// - algorithm has to be chosen
// It enables or disables the button accordingly.
function validateTravelItinerary(daysNumber, objectivesButtons, generateButton, daysButtonsChecked, algorithmsButtonsChecked) {
        
    // Initially, number of touristic objectives checked is 0
    let buttonsChecked = 0

    // Find how many touristic objectives are checked
    objectivesButtons.forEach(otherObjectiveButton => {
        if (otherObjectiveButton.checked) {
            buttonsChecked ++;
        }
    });

    // Check conditions to be satisfied
    if (buttonsChecked >= daysNumber && algorithmsButtonsChecked && daysButtonsChecked) {
        generateButton.disabled = false
        styleEnabledButton(generateButton)
    }
    else {
        generateButton.disabled = true
        styleDisabledButton(generateButton)
    }
}

// Function extracts travel itinerary buttons and detects changes
function getTravelItineraryButtons() {
    // Get days radio buttons
    const daysButtons = document.querySelectorAll(".travel-itineraries__day-radio")
    // Get algorithms radio buttons
    const algorithmsButtons = document.querySelectorAll(".travel-itineraries__algorithm-radio")
    // Get touristic objectives checkbox buttons
    const objectivesButtons = document.querySelectorAll(".travel-itineraries__objective-checkbox")

    // Get generate button
    const generateButton = document.querySelector(".travel-itineraries__generate-button")

    // Boolean variables 
    let daysButtonsChecked = false
    let algorithmsButtonsChecked = false
    
    // Initial number of days
    let daysNumber = 0

    // Determine wheter a radio button for days has been checked or not
    daysButtons.forEach(dayButton => {
        dayButton.addEventListener("change", function() {
            // Get nummber of days chosen
            daysNumber = dayButton.value
            
            // If a radio button is checked, then condition is satisfied
            if (dayButton.checked && daysButtonsChecked == false) {
                daysButtonsChecked = true
            }

            // Case: user changed the number of days or the number of days is his last choice
            validateTravelItinerary(daysNumber, objectivesButtons, generateButton, daysButtonsChecked, algorithmsButtonsChecked)
        });
    });

    // Determine wheter a radio buttons for algorithms has been checked or not
    algorithmsButtons.forEach(algorithmButton => {
        algorithmButton.addEventListener("change", function() {
           // If a radio button is checked, then the condition is satisfied
            if (algorithmButton.checked && algorithmsButtonsChecked == false) {
                algorithmsButtonsChecked = true
            }

            // Case: user changed the algortihm or the algorithm is his last choice
            validateTravelItinerary(daysNumber, objectivesButtons, generateButton, daysButtonsChecked, algorithmsButtonsChecked)
        });
    });

    // Determine wheter there are enough touristic objectives checked
    objectivesButtons.forEach(objectiveButton => {
        objectiveButton.addEventListener("change", function() {

            // Case: user changed the number of touristic objectives or the number of tourisitc 
            // objectives is his last choice
            validateTravelItinerary(daysNumber, objectivesButtons, generateButton, daysButtonsChecked, algorithmsButtonsChecked)
        });
    });

}

// Function displays algorithm details
function displayAlgorithmInformation() {
    // Get info icons
    const cardinalDirectionsIcon = document.getElementById("info-1")
    const kMeansIcon = document.getElementById("info-2")

    // Get info containers
    const cardinalDirectionsInfo = document.getElementById("details-1")
    const kMeansInfo = document.getElementById("details-2")

    cardinalDirectionsIcon.addEventListener("click", function() {
        cardinalDirectionsInfo.classList.toggle("active")
    });

    kMeansIcon.addEventListener("click", function() {
        kMeansInfo.classList.toggle("active")
    })
}

// Function displays the remaining characters for the name and the description of the travel itinerary
function displayCharactersLeft() {
    // Set maximum lengths
    const nameMaxLength = 64
    const descriptionMaxLength = 256

    // Get input elements
    const nameInput = document.querySelector(".optional__name-input")
    const descriptionInput = document.querySelector(".optional__description-input")

    // Get elements for display
    const nameCharactersRemaining = document.querySelector(".optional__name-input-remaining")
    const descriptionCharactersRemaining = document.querySelector(".optional__description-input-remaining")

    // Add event listener for every input elements

    // For name
    nameInput.addEventListener("input", function() {
        // Extract text review
        const name = nameInput.value

        // Case: nothing found
        if (name === "") {
            nameCharactersRemaining.innerHTML = "Characters left: 64"
        }
        // Case: user writes
        else {
            // Calculate the difference
            const diff = nameMaxLength - name.length

            // Change color when no character remained
            if (diff == 0) {
                nameCharactersRemaining.style.color = "#D47E73"
            }
            if (diff == 1) {
                nameCharactersRemaining.style.color = "#8C98AD"
            }
            
            // Display the remaining characters
            nameCharactersRemaining.innerHTML = "Characters left: " + diff.toString()
        }
    });

    // For description
    descriptionInput.addEventListener("input", function() {
        // Extract text review
        const description = descriptionInput.value

        // Case: nothing found
        if (description === "") {
            descriptionCharactersRemaining.innerHTML = "Characters left: 256"
        }
        // Case: user writes
        else {
            // Calculate the difference
            const diff = descriptionMaxLength - description.length

            // Change color when no character remained
            if (diff == 0) {
                descriptionCharactersRemaining.style.color = "#D47E73"
            }
            if (diff == 1) {
                descriptionCharactersRemaining.style.color = "#8C98AD"
            }
            
            // Display the remaining characters
            descriptionCharactersRemaining.innerHTML = "Characters left: " + diff.toString()
        }
    });
}


/* STATISTICS */
// Function creates average grades graph
function createGradesGraph() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".statistics__line")

    // Define average grade per field array
    const gradePerField = []

    // Extract average grade from grade attribute
    graphLines.forEach(graphLine => {
        gradePerField.push(graphLine.getAttribute("grade"))
        graphLine.removeAttribute("grade")
     });

    // Set specific heights and colors for graph lines
    for (let index = 0; index < gradePerField.length; index++) {   
        // 10% -> statistics__field, 10% -> statistics__line-number => maximum height is 80% 
        let height = gradePerField[index] * 8

        // Set height
        graphLines[index].style.height = height.toString() + "%"

        // Set color after grade
        // Less than 5
        if (height < 40) {
            graphLines[index].classList.add("bad")
        }
        // Between 5 and 7.5
        if (height >= 40 && height < 60) {
            graphLines[index].classList.add("good")
        }
        // Bigger than 7.5
        if (height >= 60) {
            graphLines[index].classList.add("perfect")
        }
    }
}


/* REVIEWS */
// Function sets different colors for profile pictures of the users
// which do not have one
function setProfilePictureColors() {
    const profilePicturesLike = document.querySelectorAll(".profile__photo-like")

    // Check if there are profile pictures like and proceed accrodingly
    if (profilePicturesLike.length > 0) {
        profilePicturesLike.forEach(profilePictureLike => {
            // Randomize
            let colorOption = Math.floor(Math.random() * 3)
            // Set color
            if (colorOption == 0) {
                profilePictureLike.classList.add("one")
            }
            if (colorOption == 1) {
                profilePictureLike.classList.add("two")
            }
            if (colorOption == 2) {
                profilePictureLike.classList.add("three")
            }
        });
    }
}


/* OTHERS */
// Function disables action buttons starting with the second click made
function disableActionButtons() {
     // Get action buttons
     const addToWishlist = document.querySelector(".destination__button-wishlist")
     const markAsVisited = document.querySelector(".destination__button-visited")
     // Variables to know when a second click is made
     let secondClickWishlist = 0
     let secondClickVisited = 0
 
     addToWishlist.addEventListener("click", function() {
        // Disable the other action button
        markAsVisited.disabled = true

        secondClickWishlist++;
        // On second click, disable the button
        if (secondClickWishlist == 2) {
            addToWishlist.disabled = true
         }
     });
     markAsVisited.addEventListener("click", function() {
        // Disable the other action button
        addToWishlist.disabled = true

        secondClickVisited++;
        if (secondClickVisited == 2) {
            markAsVisited.disabled = true
         }
     });
}

// Function applies a specific style to the sticky element when it reaches the top of the page.
function setStyleToStickyElement () {
    // Get sticky element
    const stickyElement = document.querySelector(".destination__middle-container")

    let isAtTheTop = false

    // Change style if sticky element is already at the top
    // Get sticky element position
    positions = stickyElement.getBoundingClientRect()
    // If sticky element at the top, apply style
    if (positions.top == 0) {
        if (isAtTheTop == false) {
            stickyElement.style.boxShadow = "0rem 0.25rem 1rem #D47E73"
            isAtTheTop = true
        }
    }

    // Change style if window was scrolled
    document.addEventListener("scroll", () => {
        // Get sticky element position
        positions = stickyElement.getBoundingClientRect()
        
        // When sticky element is at the top, apply style
        if (positions.top == 0) {
            if (isAtTheTop == false) {
                stickyElement.style.boxShadow = "0rem 0.25rem 1rem #D47E73"
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

// Function closes the modal when the user clicks on the close button.
function exitModal() {
    // Get modal
    const modal = document.querySelector(".modal")

    // Case: no modal displayed
    if (modal == null) {
        return
    }

    // Get background element
    const background = document.querySelector(".modal__background-grey")

    // Get close button
    const closeButton = document.querySelector(".modal__button.close")
    
    // Add event listener for button
    closeButton.addEventListener("click", function() {
        // Hide them
        modal.close()
        background.classList.add("inactive")
    });
}


// Function moves HTML element inside another container to ensure the responsiveness of the website
function responsiveLayout() {
    // Only when screen width <= 600
    if (window.innerWidth <= 600) {
        // Get elements to be moved
        const toBeMoved = document.querySelectorAll(".reviews__bottom-details")

        // Get container elements
        const container = document.querySelectorAll(".reviews__review-card")

        // Move every element inside the desired container
        for (let index = 0; index < toBeMoved.length; index++) {
            container[index].insertBefore(toBeMoved[index], container[index].children[1])
        }
    }
    else {
        // Get elements to be moved
        const toBeMoved = document.querySelectorAll(".reviews__bottom-details")

        // Get container elements
        const container = document.querySelectorAll(".reviews__details")

        // Move every element inside the desire container
        for (let index = 0; index < toBeMoved.length; index++) {
            container[index].appendChild(toBeMoved[index])
        }
    }
}


//
function ascendentSorting(dateOne, dateTwo) {
    if (dateOne.getAttribute("published_date") < dateTwo.getAttribute("published_date"))
        return - 1
    if (dateOne.getAttribute("published_date") > dateTwo.getAttribute("published_date"))
        return 1
    return 0
}


// Function ensures dropdown menus style for filter options and the filtering
function filterReviews() {
    // Get filter buttons
    const buttons = document.querySelectorAll(".filter__options-button")

    // Get dropdown menus
    const dropdownMenus = document.querySelectorAll(".filter__dropdown-container")

    // Get filter options buttons
    const optionButtons = document.querySelectorAll(".filter__option-radio")

    // Change styles on click
    for (let index = 0; index < buttons.length; index++) {

        buttons[index].addEventListener("click", function() {

            // Close the last opened dropdown menu
            dropdownMenus.forEach(dropdownMenu => {
                if (dropdownMenu != dropdownMenus[index] && dropdownMenu.classList.contains("active")) {
                    dropdownMenu.classList.remove("active")
                }
            });

            // Change style for last button pressed 
            buttons.forEach(button => {
                if (button != buttons[index] && button.classList.contains("active")) {
                    button.classList.remove("active")
                }
            });
            
            // Change style for new button pressed
            buttons[index].classList.toggle("active")
            // Open correspondent dropdown menu
            dropdownMenus[index].classList.toggle("active")
        });
    }

    // Change styles on new radio button checked
    for (let index = 0; index < optionButtons.length; index++) {

        optionButtons[index].addEventListener("change", function() {
         
            // Uncheck last checked radio button
            for (let index2 = 0; index2 < optionButtons.length; index2++) {
                
                if (index != index2 && optionButtons[index2].checked == true) {
                    optionButtons[index2].checked = false
                }
            }
            
            // Change styles
            if ([0, 1].includes(index)) {
                // Close current dropdown menu
                dropdownMenus[0].classList.remove("active")

                // Change style for current button pressed
                buttons[0].classList.remove("active")
            }
            if ([2, 3].includes(index)) {
                // Close current dropdown menu
                dropdownMenus[1].classList.remove("active")

                // Change style for current button pressed
                buttons[1].classList.remove("active")
            }
            if ([4, 5].includes(index)) {
                // Close current dropdown menu
                dropdownMenus[2].classList.remove("active")

                // Change style for current button pressed
                buttons[2].classList.remove("active")
            }

            // Get reviews container
            const reviewsContainer = document.querySelector(".reviews__content")

            // Get reviews cards
            const reviews = document.querySelectorAll(".reviews__review-card")
            // Create array with review cards
            const arrayReviews = Array.from(reviews)

            // Determine filter chosen and proceed accordingly
            if (optionButtons[index].name == "level") {
                if (optionButtons[index].value == "Highest to lowest") {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        levelOne = elementOne.getAttribute("traveler_level")
                        levelTwo = elementTwo.getAttribute("traveler_level")

                        // Check which is bigger
                        if (levelOne < levelTwo) {
                            return -1
                        }
                        if (levelOne > levelTwo) {
                            return 1
                        }
                        if (levelOne == levelTwo) {
                            return 0
                        }
                    });
                }
                else {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        levelOne = elementOne.getAttribute("traveler_level")
                        levelTwo = elementTwo.getAttribute("traveler_level")

                        console

                        // Check which is bigger
                        if (levelOne < levelTwo) {
                            return 1
                        }
                        if (levelOne > levelTwo) {
                            return -1
                        }
                        if (levelOne == levelTwo) {
                            return 0
                        }
                    });
                }
            }
            if (optionButtons[index].name == "feeling") {
                if (optionButtons[index].value == "Best to worst") {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        feelingOne = elementOne.getAttribute("general_feeling")
                        feelingTwo = elementTwo.getAttribute("general_feeling")

                        // Check which is bigger
                        if (feelingOne < feelingTwo) {
                            return -1
                        }
                        if (feelingOne > feelingTwo) {
                            return 1
                        }
                        if (feelingOne == feelingTwo) {
                            return 0
                        }
                    });
                }
                else {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        feelingOne = elementOne.getAttribute("general_feeling")
                        feelingTwo = elementTwo.getAttribute("general_feeling")

                        console

                        // Check which is bigger
                        if (feelingOne < feelingTwo) {
                            return 1
                        }
                        if (feelingOne > feelingTwo) {
                            return -1
                        }
                        if (feelingOne == feelingTwo) {
                            return 0
                        }
                    });
                }
            }
            if (optionButtons[index].name == "date") {
                if (optionButtons[index].value == "Descending") {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        dateOne = elementOne.getAttribute("published_date")
                        dateTwo = elementTwo.getAttribute("published_date")

                        // Check which is bigger
                        if (dateOne < dateTwo) {
                            return -1
                        }
                        if (dateOne > dateTwo) {
                            return 1
                        }
                        if (dateOne == dateTwo) {
                            return 0
                        }
                    });
                }
                else {
                    // Sort reviews
                    arrayReviews.sort((elementOne, elementTwo) => {
                        // Extract attribute values
                        dateOne = elementOne.getAttribute("published_date")
                        dateTwo = elementTwo.getAttribute("published_date")

                        // Check which is bigger
                        if (dateOne < dateTwo) {
                            return 1
                        }
                        if (dateOne > dateTwo) {
                            return -1
                        }
                        if (dateOne == dateTwo) {
                            return 0
                        }
                    });
                }
            }

            // Add reviews to reviews container in a new order
            arrayReviews.forEach(review => {
                reviewsContainer.appendChild(review)
            });
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
    
    // Get search bar
    const searchBar = document.querySelector(".travel-itineraries__input")
    // Add an event listener for search bar
    searchBar.addEventListener("input", () => returnTouristicObjectives(searchBar))

    // Order: after importance
    disableActionButtons()
    exitModal()
    setStyleToStickyElement()
    createGradesGraph()
    getTravelItineraryButtons()
    displayAlgorithmInformation()
    filterReviews()
    setProfilePictureColors()
    displayCharactersLeft()
    
    // First time check
    responsiveLayout()

    // Add an event listener to know when window resizes
    window.addEventListener("resize", () => responsiveLayout())
  });