/* GENERAL */

// Function modifies menu icon for phone
function modifyMenuIcon() {
    // TODO -> delete next line
    console.log("Intra si in modifyPhoneMenu")

    // Get menu bars
    const menuBars = document.querySelectorAll(".phone-menu-icon-bar")

    // Modify menu bars by adding CSS new class / remove CSS new class
    menuBars.forEach(menuBar => {
            menuBar.classList.toggle("active")
    });

}

// Function opens / closes phone menu
function displayPhoneMenu() {
    // TODO -> delete next line
    console.log("Intra in displayPhoneMenu")
}

// Start after HTML code is rendered
window.addEventListener("load", function() {
    // Get menu
    const menu = document.querySelector(".phone-menu-icon-container")
    
    // Add event listener for menu
    menu.addEventListener("click", () => {
        modifyMenuIcon()
        displayPhoneMenu()
    });
  });