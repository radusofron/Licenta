// Function returns the destinations which match the search
function returnDestinations() {
  // Get destinations
  const destinations = document.querySelectorAll(".all-destinations__destination")

  // Get search bar input
  const inputExtracted = document.querySelector(".all-destinations__input").value
  // Transform input to lowercase input
  const input = inputExtracted.toLowerCase()

  // Check if input is empty; if so, display all the destinations again and stop
  if (input.trim() === "") {
    destinations.forEach(destination => {
       // If destination is inactive, make it active
      if (destination.classList[1] === "inactive") {
        destination.classList.remove("inactive");
      }
    });
    return
  }

  // Variable used to know if no destination will be returned
  let minimumADestinationReturned = false

  // Get element used for no results found message
  const noResultsMessage = document.querySelector(".all-destinations__search-results-not-found")

  // Search for matches
  destinations.forEach(destination => {
    // Extract destination from HTML
    const destinationName = destination["children"][1].textContent.toLowerCase()

    // Trim the strings in order to compare them
    if (destinationName.trim() === input.trim() || destinationName.trim().startsWith(input.trim()) || destinationName.trim().endsWith(input.trim())) {
      // If destination is inactive, make it active
      if (destination.classList[1] === "inactive"){
        destination.classList.remove("inactive");
      }
    }
    else {
      // If destination is active, make it inactive
      if (destination.classList[1] !== "inactive") {
        destination.classList.add("inactive");
      }
    }
    // Check if there is at least a destination which will be displayed (does not have "inactive" class)
    if (!destination.classList.contains("inactive")) {
      minimumADestinationReturned = true
    }
  });

  // Check if no results were found in order to display appropiate message
  if (minimumADestinationReturned) {
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


// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get search bar
    const searchBar = document.querySelector(".all-destinations__input")

    // Add an event listener for search bar
    searchBar.addEventListener("input", () => returnDestinations(searchBar))
  });