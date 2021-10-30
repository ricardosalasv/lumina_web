function main(){
    
    var fpShapeContainer = document.querySelector("#fpShapeContainer")
    fpShapeContainer.addEventListener("mouseup", fpShapeDetector)

    // Locking all the room's dimension fields at first
    roomDimensionFields = [
        document.querySelector("input[name=roomLength]"),
        document.querySelector("input[name=roomWidth]"),
        document.querySelector("input[name=roomHeight]"),
        document.querySelector("input[name=roomArea]")
    ]

    roomDimensionFields.forEach(function(element){
        element.classList.add("lockedField")
    })

    // Adding onfocusout event to the room's length, and width fields
    var regularFpOptions = document.querySelectorAll(".regularFpOptions")
    regularFpOptions.forEach(function(i){
        i.addEventListener("focusout", calculateArea)
    })

    // Adding onfocusout event to the room's area in order to have data in the width and length and being able to submit the form
    document.querySelector("input[name=roomArea]").addEventListener("focusout", calculateDimensions)

    // Implementing model filtering based on selected brand
    document.querySelector("select[name=brand]").addEventListener("change", filterModels)

    // Executing filterModels() at least once at the beginning
    filterModels()

    // Displaying relevant data from the selected fixture model
    document.querySelector("select[name=brand").addEventListener("change", showFixtureData)
    document.querySelector("select[name=fixtureModel").addEventListener("change", showFixtureData)

    // Executing showFixtureData() at least once at the beginning
    showFixtureData()

    // Executing AJAX request to calculate the project result on the backend 
    // and then return the relevant data to be displayed in the frontend
    document.querySelector("input[name=calculate]").addEventListener("mouseup", CalculateProject)
    
}

// Locks or unlocks the Room's dimensions fields based on the selected Shape Option
function fpShapeDetector(){

    var fpShapeSelection = document.querySelector('input[name="floorplanShape"]:focus').value
    var irregularFpOptions = document.querySelectorAll(".irregularFpOptions")
    var regularFpOptions = document.querySelectorAll(".regularFpOptions")

    if (fpShapeSelection == "Rectangular"){

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
    else{

        irregularFpOptions.forEach(function(i){
            i.classList.remove("lockedField")
        })

        regularFpOptions.forEach(function(i){
            i.classList.add("lockedField")
            i.classList.add("grayText")
        })
    }

    // Unlocks the height field if run for the first time
    heightField = document.querySelector("input[name=roomHeight]")

    if (heightField.classList.contains("lockedField")) {
        heightField.classList.remove("lockedField")
    }

}

// Calculates the Room area automatically if the floor plan shape is Rectangular
function calculateArea(){

    var fpShapeSelection = document.querySelector('input[name="floorplanShape"]:checked').value

    if (fpShapeSelection == "Rectangular"){

        try {
            var roomLength = parseInt(document.querySelector('input[name=roomLength]').value)
        } catch (error) {
            var roomLength = 0
        }
    
        try {
            var roomWidth = parseInt(document.querySelector('input[name=roomWidth]').value)
        } catch (error) {
            var roomWidth = 0
        }
    
        try {
            var roomArea = roomLength * roomWidth
        } catch (error) {
            var roomArea = null
        }
    
        if (!roomArea) {
            roomArea = null
        }

        var areaField = document.querySelector('input[name=roomArea]')
        areaField.value = roomArea
    }

}

function calculateDimensions(){
    var roomArea = document.querySelector("input[name=roomArea]").value

    var roomDimensions = Math.sqrt(roomArea)
    roomDimensions = Math.round(roomDimensions)

    var regularFpOptions = document.querySelectorAll(".regularFpOptions")
    regularFpOptions.forEach(function(i){
        i.value = roomDimensions
    })
}

function filterModels(){

    var selectedBrand = document.querySelector('select[name=brand]').value

    for (var brand of Object.entries(fixtureList)) {

        if (brand[0] == selectedBrand) {

            var listOfModels = ""

            for (var model of brand[1]){
                listOfModels += `<option value = "${model.name}">${model.name}</option>`
            }
        
        }
        
        document.querySelector('select[name=fixtureModel]').innerHTML = listOfModels
    }

}

function showFixtureData(){

    var priceField = document.querySelector('input[name=fixtureCost]')
    var finishField = document.querySelector('input[name=fixtureFinish]')
    var lumenField = document.querySelector('input[name=fixtureLumens]')

    var selectedBrand = document.querySelector('select[name=brand]').value
    var selectedModel = document.querySelector('select[name=fixtureModel]').value

    for (var brand of Object.entries(fixtureList)) {

        if (brand[0] == selectedBrand) {

            for (var model of brand[1]) {

                if (model.name == selectedModel) {

                    priceField.value = model.price
                    finishField.value = model.finish
                    lumenField.value = model.lm

                }

            }

        }

    }
}

function CalculateProject(){

    var dataToSubmit = {
        floorplanShape : document.querySelector("input[name=floorplanShape]:checked").value,
        roomLength : document.querySelector("input[name=roomLength]").value,
        roomWidth : document.querySelector("input[name=roomWidth]").value,
        roomHeight : document.querySelector("input[name=roomHeight]").value,
        roomArea : document.querySelector("input[name=roomArea]").value,
        roomCeilingMaterial : document.querySelector("select[name=roomCeilingMaterial]").value,
        roomWallMaterial : document.querySelector("select[name=roomWallMaterial]").value,
        roomFloorMaterial : document.querySelector("select[name=roomFloorMaterial]").value,
        luxRequirement : document.querySelector("input[name=luxRequirement]").value,
        lightingPlaneHeight : document.querySelector("input[name=lightingPlaneHeight]").value,
        brand : document.querySelector("select[name=brand]").value,
        fixtureModel : document.querySelector("select[name=fixtureModel]").value,
        fixtureLumens : document.querySelector("input[name=fixtureLumens]").value,
        fixtureFinish : document.querySelector("input[name=fixtureFinish]").value,
        fixtureCost : document.querySelector("input[name=fixtureCost]").value,
        projectId : project["id"],
        projectCode : project["projectCode"]
    }
    console.log(dataToSubmit)

    $.ajax({
            url: '/project',
            data: dataToSubmit,
            dataType: 'json',
            type: 'PUT',
            success: function(response){
                document.querySelector("#AmountOfFixtures").innerHTML = response.AmountOfFixtures.toString()
                document.querySelector("#ProjectCost").innerHTML = response.ProjectCost.toString()

                return response
            },
            error: function(error){
                console.log(error)
                return 0
            }
        })
}

document.addEventListener("DOMContentLoaded", main)


