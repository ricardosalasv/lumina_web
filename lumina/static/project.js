function main(){
    
    console.log(project)
    console.log(fixtureList)
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
        })


    }
    else{

        irregularFpOptions.forEach(function(i){
            i.classList.remove("lockedField")
        })

        regularFpOptions.forEach(function(i){
            i.classList.add("lockedField")
            i.value = null
        })
    }

    // Unlocks the height field if run for the first time
    heightField = document.querySelector("input[name=roomHeight]")

    console.log(heightField.classList)

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
    
        console.log(roomLength)
    
        try {
            var roomWidth = parseInt(document.querySelector('input[name=roomWidth]').value)
        } catch (error) {
            var roomWidth = 0
        }
    
        console.log(roomLength)
    
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

    console.log(roomArea)

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

    var serializedForm = $("form").serialize()

    $.ajax({
            url: '/project',
            data: serializedForm,
            type: 'PUT',
            success: function(response){
                console.log(response)

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


