/* CONTENT LOADS / STYLES DINAMICALLY */

// Function finds the section containing a class named "active"
function findActiveSection(sections) {
    targetClassName = "active"
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

// Function finds the header option containing a class named "active" if exists one
function findActiveOption() {
    activeOption = document.querySelector(".header-option.active")
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


/* RESPONSIVE */

// Function opens / closes phone menu
function displayPhoneMenu() {
    // Get header background for phone menu & phone menu
    const phoneMenu = document.querySelector(".phone-menu")
    const header = document.querySelector(".header-background")

    // Display phone menu by adding CSS new class / removing CSS new class
    phoneMenu.classList.toggle("active")
    header.classList.toggle("active")
}


/* GENERAL */

// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get header options
    const defaultOption = document.querySelector(".site-name")
    const otherOptions = document.querySelectorAll(".header-option")
    // Create an array with them
    const options = Array.from(otherOptions).concat(defaultOption)

    // Get sections
    const sections = document.querySelectorAll(".section")

    // Add an event listener for every header option
    options.forEach(option => {
            option.addEventListener("click", () => displayOptionAndSection(option, sections))
        });

    // Get menu
    const menu = document.querySelector(".phone-menu-icon-container")
    menu.addEventListener("click", () => displayPhoneMenu())
  });