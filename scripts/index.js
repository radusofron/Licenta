/* Code for enabling scrolling option after 6 seconds */
const mainContainer = document.querySelector("main.container-for-sections");
function enableScrolling() {
    mainContainer.style["overflow-y"] = 'scroll';
}
setTimeout(enableScrolling, 3500);



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
    if (activeImageClass === "photo-container photo-container--1")
    {
        nextActiveImage = document.querySelector(".photo-container--2");
    }
    else {
        if (activeImageClass === "photo-container photo-container--2")
        {
            nextActiveImage = document.querySelector(".photo-container--3");
        }
        else {
            if (activeImageClass === "photo-container photo-container--3")
            {
                nextActiveImage = document.querySelector(".photo-container--4");
            }
            else {
                nextActiveImage = document.querySelector(".photo-container--1");
            }
        }

    }
    nextActiveImage.setAttribute(attribute, "");
}
let intervalIdForPhotos = setInterval(changePhoto, 7000);
// let intervalIdForStartTheJourney = null;
let alreadyOnViewport = true;
let alreadyOutOfViewport = false;



/* Code to determine if a section is in the viewport or not */
// extract user's viewport height and width
const userHeight = document.documentElement.clientHeight;
const userWidth = document.documentElement.clientWidth;
// extract main container's sections & their height
const sections = [];
const sectionsNumber = 6;
const sectionsClasses = [".section--first-section", ".section--second-section", ".section--third-section", ".section--fourth-section", ".section--fifth-section", ".section--sixth-section"];
const sectionsHeights = [];
for (let i = 0; i < sectionsNumber; i++){
    sections[i] = document.querySelector(sectionsClasses[i]);
    sectionsHeights[i] = sections[i].getBoundingClientRect().height;
}
// stores true if the section was visited
const sectionsVisited = [];
for (let i = 0; i < sectionsNumber; i++){
    sectionsVisited[i] = false;
}

// check when to run continuous animations of section 1 -> ebery time the section is in the viewport
function firstSectionAnimations(liveFirstSectionY, firstSectionHeight) {

    // now in the first section
    if (liveFirstSectionY >= 0 && liveFirstSectionY <= firstSectionHeight)
    {
        if(alreadyOnViewport == false)
        {
            // turn on "changing" photo slider
            intervalIdForPhotos = setInterval(changePhoto, 7000);    
            alreadyOnViewport = true;
            alreadyOutOfViewport = false;

            // turn on "pop up" start the journey button
            startTheJourney = document.querySelector(".text-container__sign-up-button");
            startTheJourney.style.animationPlayState = 'running';
        }
    }
    //  not anymore in the first section
    else{
        if (alreadyOutOfViewport == false)
        {
            // turn off "changing" photo slider
            clearInterval(intervalIdForPhotos);
            alreadyOnViewport = false;
            alreadyOutOfViewport = true;

            // turn off "pop up" start the journey buttom
            startTheJourney = document.querySelector(".text-container__sign-up-button");
            startTheJourney.style.animationPlayState = 'paused';
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
        let leftIconContainers = document.querySelectorAll(".intro-for-about__icon-container.intro-for-about__icon-container--left");
        for (let i = 0; i < leftIconContainers.length; i++){
            leftIconContainers[i].style.animation = 'about-from-left-animation 1.5s';
        }
        let rightIconContainers = document.querySelectorAll(".intro-for-about__icon-container.intro-for-about__icon-container--right");
        for (let i = 0; i < rightIconContainers.length; i++){
            rightIconContainers[i].style.animation = 'about-from-right-animation 1.5s';
        }
        let textContainers = document.querySelectorAll(".title-container__title, .description-container__description");
        for (let i = 0; i < textContainers.length; i++){
            textContainers[i].style.animation = 'about-text-animation 1s';
        }

        sectionsVisited[1] = true;
    }
}

function thirdSectionAnimations(liveThirdSectionY, thirdSectionHeight){
    // FIXME -> to be 0
    // now in the third section
    if (liveThirdSectionY >= -1 && liveThirdSectionY < (thirdSectionHeight - 1))
    {
        // extract elements which will contain animations
        let introText = document.querySelector(".content__about-intro-text");
        introText.style.animation = 'about-2-from-left-animation 1s';
        let infoCards = document.querySelectorAll(".about-card");
        for (let i = 0; i < infoCards.length; i++){
            infoCards[i].style.animation = 'about-2-cards-animation 2s';
        }
        let leftDesignElements = document.querySelectorAll(".left-blur");
        for (let i = 0; i < leftDesignElements.length; i++){
            leftDesignElements[i].style.animation = 'about-2-from-left-2-animation 2.5s';
        }
        let rightDesignElements = document.querySelectorAll(".right-blur");
        for (let i = 0; i < rightDesignElements.length; i++){
            rightDesignElements[i].style.animation = 'about-2-from-right-animation 2.5s';
        }
        
        sectionsVisited[2] = true;
    }
}

// scroll listener for the main container
mainContainer.addEventListener('scroll', function() {

    // extract sections' current position compared to the viewport
    liveSectionsY = [];
    for (let i = 0; i < sectionsNumber; i++){
        liveSectionsY[i] = sections[i].getBoundingClientRect().y;
    }
    
    // animations for first section
    firstSectionAnimations(liveSectionsY[0], sectionsHeights[0]);

    // animations for second section
    if (sectionsVisited[1] == false){
        secondSectionAnimations(liveSectionsY[1], sectionsHeights[1]);
    }
    if (sectionsVisited[2] == false){
        thirdSectionAnimations(liveSectionsY[2], sectionsHeights[2]);
    }
});