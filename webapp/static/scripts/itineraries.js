// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get every open button
    const buttons = document.querySelectorAll(".itineraries__open-button")

    // Get every itinerary text container
    const containers = document.querySelectorAll(".itineraries__itinerary-text")

    let number = 0
    // Add different backgrounds.
    for (let index = 0; index <= buttons.length; index++) {
        if (number % 5 == 0) {
            buttons[index].style.backgroundColor = "#608DB8"
            containers[index].style.borderRight = "1.5rem solid #608DB8"
        }
        if (number % 5 == 1) {
            buttons[index].style.backgroundColor = "#7EBDC2"
            containers[index].style.borderRight = "1.5rem solid #7EBDC2"
        }
        if (number % 5 == 2) {
            buttons[index].style.backgroundColor = "#8C98AD"
            containers[index].style.borderRight = "1.5rem solid #8C98AD"
        }
        if (number % 5 == 3) {
            buttons[index].style.backgroundColor = "#C4A4A4"
            containers[index].style.borderRight = "1.5rem solid #C4A4A4"
        }
        if (number % 5 == 4) {
            buttons[index].style.backgroundColor = "#D47E73"
            containers[index].style.borderRight = "1.5rem solid #D47E73"
        }
        number++
    }
  });