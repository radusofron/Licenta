// FIXME - make it simpler

function setTimeToChange() {
    setTimeout(changePhoto, 5000);
}

function changePhoto() {
    // attribute name
    const attribute = "active-image"
    // extract html element with attribute [active-image]
    let activeImage = document.querySelector("[active-image]");
    // extract class for the above html element
    let activeImageClass = activeImage.getAttribute('class');
    // remove attribute for the above html element and add it to the next html element
    if (activeImageClass === "photo-container photo-container-1")
    {
        activeImage.removeAttribute(attribute);
        const nextActiveImage = document.querySelector(".photo-container-2");
        nextActiveImage.setAttribute(attribute, ""); 
    }
    else {
        if (activeImageClass === "photo-container photo-container-2")
        {
            activeImage.removeAttribute(attribute);
            const nextActiveImage = document.querySelector(".photo-container-3");
            nextActiveImage.setAttribute(attribute, ""); 
        }
        else {
            if (activeImageClass === "photo-container photo-container-3")
            {
                activeImage.removeAttribute(attribute);
                const nextActiveImage = document.querySelector(".photo-container-4");
                nextActiveImage.setAttribute(attribute, ""); 
            }
            else {
                activeImage.removeAttribute(attribute);
                const nextActiveImage = document.querySelector(".photo-container-1");
                nextActiveImage.setAttribute(attribute, ""); 
            }
        }

    }
    setTimeToChange();
}

setTimeout(setTimeToChange, 3000);