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

// Function removes class named "active"
function removeActiveSection(section) {
    section.classList.remove("active")
}

// Function adds class named "active"
function addActiveSection(section) {
    section.classList.add("active")
}

// Function starts when an option is clicked
function option_display(option, sections) {
    const activeSection = findActiveSection(sections)
    removeActiveSection(activeSection)
    sections.forEach(section => {
        if (section.classList[1] === option.classList[1]){
            wantedSection = section
        }
    });
    addActiveSection(wantedSection)
}

// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get header options
    const defaultOption = document.querySelector(".site-name")
    const otherOptions = document.querySelectorAll(".header-option")
    // Create an array with them
    const options = Array.from(otherOptions).concat(defaultOption)

    // Get sections
    const sections = this.document.querySelectorAll(".section")

    // Add an event listener for every header option
    options.forEach(option => {
            option.addEventListener("click", () => option_display(option, sections))
        });
  });