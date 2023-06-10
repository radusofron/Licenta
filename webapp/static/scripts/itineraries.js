// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get every open button
    const itineraries = document.querySelectorAll(".itineraries__open-button")

    let number = 0
    // Add different backgrounds.
    itineraries.forEach(itinerary => {
        if (number % 5 == 0) {
            itinerary.style.backgroundColor = "#608DB8"
        }
        if (number % 5 == 1) {
            itinerary.style.backgroundColor = "#7EBDC2"
        }
        if (number % 5 == 2) {
            itinerary.style.backgroundColor = "#8C98AD"
        }
        if (number % 5 == 3) {
            itinerary.style.backgroundColor = "#C4A4A4"
        }
        if (number % 5 == 4) {
            itinerary.style.backgroundColor = "#D47E73"
        }
        number++
    });
  });