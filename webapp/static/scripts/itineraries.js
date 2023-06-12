// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get every open button
    const buttons = document.querySelectorAll(".itineraries__open-button")

    // Case: all itineraries
    if (buttons.length != 0) {
        // Get every itinerary text container
        const containers = document.querySelectorAll(".itineraries__itinerary-text")

        // Add different backgrounds.
        for (let index = 0; index < buttons.length; index++) {
            if (index % 5 == 0) {
                buttons[index].style.backgroundColor = "#608DB8"
                containers[index].style.borderRight = "1.5rem solid #608DB8"
            }
            if (index % 5 == 1) {
                buttons[index].style.backgroundColor = "#7EBDC2"
                containers[index].style.borderRight = "1.5rem solid #7EBDC2"
            }
            if (index % 5 == 2) {
                buttons[index].style.backgroundColor = "#8C98AD"
                containers[index].style.borderRight = "1.5rem solid #8C98AD"
            }
            if (index % 5 == 3) {
                buttons[index].style.backgroundColor = "#C4A4A4"
                containers[index].style.borderRight = "1.5rem solid #C4A4A4"
            }
            if (index % 5 == 4) {
                buttons[index].style.backgroundColor = "#D47E73"
                containers[index].style.borderRight = "1.5rem solid #D47E73"
            }
        }
    }

    // Get every color container
    const colorContainers = document.querySelectorAll(".representation__legend-color")

    // Case: specific itinerary
    if (colorContainers.length != 0) {
        // Add different colors
        for (let index = 0; index < colorContainers.length; index++) {
            if (index == 0) {
                colorContainers[index].style.backgroundColor = "#608DB8"
            }
            if (index == 1) {
                colorContainers[index].style.backgroundColor = "#BB493A"
            }
            if (index == 2) {
                colorContainers[index].style.backgroundColor = "#FFA90A"
            }
            if (index == 3) {
                colorContainers[index].style.backgroundColor = "#3D9537"
            }
            if (index == 4) {
                colorContainers[index].style.backgroundColor = "#3B3941"
            }
            if (index == 5) {
                colorContainers[index].style.backgroundColor = "#F397D6"
            }
            if (index == 6) {
                colorContainers[index].style.backgroundColor = "#8338EC"
            }
        }
    }
  });