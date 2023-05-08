/* GENERAL */

// Function modifies menu icon for phone
function modifyMenuIcon() {

    // Get menu bars
    const menuBars = document.querySelectorAll(".phone-menu-icon-bar")

    // Modify menu bars by adding CSS new class / remove CSS new class
    menuBars.forEach(menuBar => {
            menuBar.classList.toggle("active")
    });

}

// Function opens / closes phone menu
function displayPhoneMenu() {

    // Get phone menu
    const phoneMenu = document.querySelector(".phone") 

    // Display phone menu by adding CSS new class / removing CSS new class
    phoneMenu.classList.toggle("active")
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