function main() {
    
    if (project.LoadedProject) {
        console.log(project)
        // Loading data from the existing project to each field

        // Floor plan shape
        var fpShape = document.querySelector(`input[value=${project.fpShape}]`)
        fpShape.checked = true

        var irregularFpOptions = document.querySelectorAll(".irregularFpOptions")
        var regularFpOptions = document.querySelectorAll(".regularFpOptions")

        if (fpShape.value == "Rectangular") {

            // Locking respective fields
            irregularFpOptions.forEach(function(i){
                i.classList.add("lockedField")
                i.value = null
            })
    
            regularFpOptions.forEach(function(i){
                i.classList.remove("lockedField")
                i.classList.remove("grayText")
                i.value = null
            })

        }
        else {

            // Locking respective fields
            irregularFpOptions.forEach(function(i){
                i.classList.remove("lockedField")
            })
    
            regularFpOptions.forEach(function(i){
                i.classList.add("lockedField")
                i.classList.add("grayText")
            })

        }

        // Dimension fields
        var roomLengthField = document.querySelector("input[name=roomLength]")
        var roomWidthField = document.querySelector("input[name=roomWidth]")
        var roomHeightField = document.querySelector("input[name=roomHeight]")
        var roomAreaField = document.querySelector("input[name=roomArea]")

        roomLengthField.value = project.roomLength
        roomWidthField.value = project.roomWidth
        roomHeightField.value = project.roomHeight
        roomAreaField.value = project.roomArea

        // Materials
        ceilingMaterialField = document.querySelector("select[name=roomCeilingMaterial]")
        wallMaterialField = document.querySelector("select[name=roomWallMaterial]")
        floorMaterialField = document.querySelector("select[name=roomFloorMaterial]")

        ceilingMaterialField.value = project.roomCeilingMaterial
        wallMaterialField.value = project.roomWallMaterial
        floorMaterialField.value = project.roomFloorMaterial

        // Lighting Preferences
        luxRequirement = document.querySelector("input[name=luxRequirement]")
        lightingPlaneHeight = document.querySelector("input[name=lightingPlaneHeight]")
        brand = document.querySelector("select[name=brand]")
        fixtureModel = document.querySelector("input[name=fixtureModel]")

        luxRequirement.value = project.luxRequirement
        lightingPlaneHeight.value = project.lightingPlaneHeight
        brand.value = project.brand

        // OUTPUTS
        document.querySelector("#AmountOfFixtures").innerHTML = project.amountOfFixtures
        document.querySelector("#ProjectCost").innerHTML = project.totalProjectCost

    }
    else {
        console.log("This is not a loaded project")
    }
}

// function loadProject(event) {

//     var clickedButton = event.target

//     // Getting the project code and project id to load the selected project
//     projectInfo = {
//         projectCode : clickedButton.getAttribute("data-projectcode"),
//         projectId : clickedButton.getAttribute("data-projectid")
//     }

//     $.ajax({
//         url: '/project',
//         data: projectInfo,
//         dataType: 'json',
//         type: 'POST',
//         success: function(response){
//             console.log(1)
//             return response
//         },
//         error: function(error){
//             console.log(error)
//             return 0
//         }
//     })

// }

document.addEventListener("DOMContentLoaded", main)