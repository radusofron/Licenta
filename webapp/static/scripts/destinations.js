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

  // Search for matches
  destinations.forEach(destination => {
    // Extract destination from HTML
    const destinationName = destination["children"][1].textContent.toLowerCase()
    // Trim the string in order to compare them
    if (destinationName.trim() === input.trim()) {
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
  });
}


// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get search bar
    const searchBar = document.querySelector(".all-destinations__input")

    // Add an event listener for search bar
    searchBar.addEventListener("input", () => returnDestinations(searchBar))
  });