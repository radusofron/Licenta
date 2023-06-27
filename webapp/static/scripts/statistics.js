// Function creates average grades graph
function createGradesGraph() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".graph__line")

    // Define average grade per city array
    const averageGradePerCity = []

    // Extract average grade from grade attribute
    graphLines.forEach(graphLine => {
        averageGradePerCity.push(graphLine.getAttribute("grade"))
        graphLine.removeAttribute("grade")
    });

    // Set specifc heights and colors for graph lines
    for (let index = 0; index < averageGradePerCity.length; index++) {
        // 10% -> graph__city, 10% -> graph__line-number => maximum height is 80% 
        let height = averageGradePerCity[index] * 8
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


// Function creates postitive reviews graph
function createReviewsGraph() {
    // Get graph lines
    const graphLines = document.querySelectorAll(".graph-2__line")

    // Define percentage per city array
    const percentagePerCity = []

    // Extract percentage from percentage attribute
    graphLines.forEach(graphLine => {
        percentagePerCity.push(graphLine.getAttribute("percentage"))
        graphLine.removeAttribute("percentage")
    });

    // Set specifc heights and colors for graph lines
    for (let index = 0; index < percentagePerCity.length; index++) {
        // 10% -> graph__city, 10% -> graph__line-number => maximum height is 80% 
        let height = percentagePerCity[index] * 80 / 100
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


// Start after HTML code is rendered
window.addEventListener("load", function() {
    
    createGradesGraph()
    createReviewsGraph()
      
  });