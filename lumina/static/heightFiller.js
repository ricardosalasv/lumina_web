function resizeSection(){

    var navBarHeight = document.querySelector("#navigationBar").clientHeight;
    var windowHeight = window.innerHeight;
    var containerFluid = document.querySelector(".container-fluid");
    var containerPadding = parseInt(window.getComputedStyle(containerFluid, null).getPropertyValue('padding-left'));

    console.log(`Navbar Height: ${navBarHeight}`)
    console.log(`Window Height: ${windowHeight}`)
    console.log(`Container Padding: ${containerPadding}`)
    console.log(`----------------------------------------------`)

    // Sets the height for the main container to fill the remaining space in the window
    document.querySelector(`#mainSection`).style.height = windowHeight - navBarHeight - (containerPadding * 2);

}

function addEventsAtDOMLoaded(){

    resizeSection();

    window.addEventListener("resize", resizeSection);
}

document.addEventListener("DOMContentLoaded", addEventsAtDOMLoaded);