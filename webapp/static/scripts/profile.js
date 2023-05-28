// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".profile__graph-line")

    // Get graph lines numbers
    const graphLinesNumbers = document.querySelectorAll(".profile__graph-number")

    // Define visited destinations per year array
    const visitedDestinationsPerYears = []

    // Extract per-year attribute values (i.e. visited destinations per year)
    graphLines.forEach(graphLine => {
        visitedDestinationsPerYears.push(graphLine.getAttribute("per-year"))
        graphLine.removeAttribute("per-year")
     });

    // Set specific heights and colors for graph lines
    for (let index = 0; index < visitedDestinationsPerYears.length; index++)
    {
        // Convert visited destinations per year from string to int
        visitedDestinationsPerYears[index] = parseInt(visitedDestinationsPerYears[index])
        if (! visitedDestinationsPerYears[index]) {
            // height
            graphLines[index].style.height = "5%"
            // color - default
        }
        else {
            // height grow coefficient
            height_coefficient = 95/35
            // height
            const height = 5 + height_coefficient * visitedDestinationsPerYears[index]
            graphLines[index].style.height = height.toString() + "%"
            // color
            graphLines[index].classList.add("contains")
            graphLinesNumbers[index].classList.add("contains")
        }
    }
  });