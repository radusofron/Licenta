/* Code for photo slider */
function changePhoto() {
    // attribute name
    const attribute = "active-image"
    // extract html element with attribute [active-image]
    let activeImage = document.querySelector("[active-image]");
    // extract class for the above html element
    let activeImageClass = activeImage.getAttribute('class');
    // remove attribute for the above html element and add it to the next html element
    activeImage.removeAttribute(attribute);
    let nextActiveImage;
    if (activeImageClass === "photo-container photo-container-1")
    {
        nextActiveImage = document.querySelector(".photo-container-2");
    }
    else {
        if (activeImageClass === "photo-container photo-container-2")
        {
            nextActiveImage = document.querySelector(".photo-container-3");
        }
        else {
            if (activeImageClass === "photo-container photo-container-3")
            {
                nextActiveImage = document.querySelector(".photo-container-4");
            }
            else {
                nextActiveImage = document.querySelector(".photo-container-1");
            }
        }

    }
    nextActiveImage.setAttribute(attribute, "");
}

// variables used for photo animation
let setIntervalID = setInterval(changePhoto, 8000);
let alreadyOnViewport = true;
let alreadyOutOfViewport = false;



/* Code for enabling scrolling option after 6 seconds */
const mainContainer = document.querySelector("main.container-for-sections");

function enableScrolling() {
    mainContainer.style["overflow-y"] = 'scroll';
}

setTimeout(enableScrolling, 7000);



/* Code to determine if a section is in the viewport or not */
// extract user's viewport height and width
const userHeight = document.documentElement.clientHeight;
const userWidth = document.documentElement.clientWidth;
// extract main container's sections & their height
const sections = [];
const sectionsNumber = 6;
const sectionsClasses = [".first-section", ".second-section", ".third-section", ".fourth-section", ".fifth-section", ".sixth-section"];
const sectionsHeights = [];
for (let index = 0; index < sectionsNumber; index++){
    sections[index] = document.querySelector(sectionsClasses[index]);
    sectionsHeights[index] = sections[index].getBoundingClientRect().height;
}
secondSectionsVisited = false;

// check when to run continuous animations of section 1 -> ebery time the section is in the viewport
function firstSectionAnimations(liveFirstSectionY, firstSectionHeight) {
    
    // extract element for site-name-color-animation
    const siteName = document.querySelector(".site-name-text");

    // now in the first section
    if (liveFirstSectionY >= 0 && liveFirstSectionY <= firstSectionHeight)
    {
        if(alreadyOnViewport == false)
        {
            // turn on "changing" photo slider
            setIntervalID = setInterval(changePhoto, 7000);    
            alreadyOnViewport = true;
            alreadyOutOfViewport = false;
            
            // turn on site-name-color-animation
            siteName.style.animationPlayState = 'running';
        }
    }
    //  not anymore in the first section
    else{
        if (alreadyOutOfViewport == false)
        {
            // turn off "changing" photo slider
            clearInterval(setIntervalID);
            alreadyOnViewport = false;
            alreadyOutOfViewport = true;

            // turn off site-name-color-animation
            siteName.style.animationPlayState = 'paused';
        }
    }
}

// check when to run the animations of section 2 -> only when second section is in the viewport for the first time
function secondSectionAnimations(liveSecondSectionY, secondSectionHeight) {
    // FIXME -> to be 0
    // now in the second section
    if (liveSecondSectionY >= -1 && liveSecondSectionY < secondSectionHeight)
    {
        // extract elements which will contain animations
        let leftIconContainers = document.querySelectorAll(".ab-icon-container.left");
        for (let i = 0; i < leftIconContainers.length; i++){
            leftIconContainers[i].style.animation = 'about-from-left-animation 3.75s';
        }
        let rightIconContainers = document.querySelectorAll(".ab-icon-container.right");
        for (let i = 0; i < rightIconContainers.length; i++){
            rightIconContainers[i].style.animation = 'about-from-right-animation 3.75s';
        }
        let textContainers = document.querySelectorAll(".ab-text-title, .ab-text-description");
        for (let i = 0; i < textContainers.length; i++){
            console.log(textContainers[i]);
            textContainers[i].style.animation = 'about-text-animation 3.75s';
        }
    }
}

// scroll listener for the main container
mainContainer.addEventListener('scroll', function() {

    // extract sections' current position compared to the viewport
    liveSectionsY = [];
    for (let index = 0; index < sectionsNumber; index++){
        liveSectionsY[index] = sections[index].getBoundingClientRect().y;
    }
    
    // animations for first section
    firstSectionAnimations(liveSectionsY[0], sectionsHeights[0]);

    // animations for second section
    if (secondSectionsVisited == false){
        secondSectionAnimations(liveSectionsY[1], sectionsHeights[1]);
        secondSectionsVisited = true;
    }
});