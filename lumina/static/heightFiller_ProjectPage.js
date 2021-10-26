function resizeSection(){

    var navBarHeight = document.querySelector("#navigationBar").clientHeight;
    var windowHeight = window.innerHeight;
    
    var summarySectionHeight = document.querySelector("#summarySection").clientHeight;

    // Sets the height for the main container to fill the remaining space in the window
    document.querySelector(`#mainSection`).style.height = windowHeight - navBarHeight;

    // Sets the height for the div reserved to be placed behind the summary section on scroll
    document.querySelector(`#summarySpaceInForm`).style.height = summarySectionHeight;
}

function resizeProjectPanels(){

    var navBarHeight = document.querySelector("#navigationBar").clientHeight;
    var windowHeight = window.innerHeight;
    
    var summarySectionHeight = document.querySelector("#summarySection").clientHeight;
    var projectTitleDivHeight = document.querySelector(".projectTitle").clientHeight;
    var calculateButtonHeight = document.querySelector("#calculateButton").clientHeight;

    var isMobile = navigator.userAgentData.mobile;

    if (!isMobile) {

        // Sets the height of the panels
        document.querySelector(`.project-panel1`).style.height = windowHeight - navBarHeight - summarySectionHeight - projectTitleDivHeight - calculateButtonHeight - 6;

    }
}

function addEventsAtDOMLoaded(){

    resizeSection();

    window.addEventListener("resize", resizeSection);
}

document.addEventListener("DOMContentLoaded", addEventsAtDOMLoaded);
document.addEventListener("DOMContentLoaded", resizeProjectPanels);