from flask.globals import session
from lumina import db
from lumina.models import Models, Arch_Materials, Projects, Floorplan_Shapes
from lumina.utilizationFactorTables import UTable, kIndexSelector
import math
import json
from datetime import datetime

def GenerateProjectCode(currentUser, projectName):

    # Creates a hash code from the user id, username, email, and project name
    usernameLen = len(currentUser.username)
    emailLen = len(currentUser.email)
    userId = currentUser.id
    projectNameLen = len(projectName)
    asciiProjectName = sum(list(map(lambda x : ord(x), projectName)))

    particularDivisor = (usernameLen + emailLen) / 16

    code = int(math.ceil((usernameLen * emailLen * userId * projectNameLen * asciiProjectName) / particularDivisor))

    # Creates prefix
    prefix = "{}{}-".format(currentUser.username.upper()[0], currentUser.username.upper()[-1])

    # Create suffix
    suffix = "-{}".format(usernameLen)

    # Generates project code
    projectCode = "{}{}{}".format(prefix, code, suffix) # RS-38424-12

    return projectCode

def CalculateProject(form, returnZero=False):

    """
    Lighting calculation based on the Lumen method
    """
    # Outputs
    AmountOfFixtures = "-"
    ProjectCost = "-"
    result = {"AmountOfFixtures" : AmountOfFixtures, 
              "ProjectCost" : ProjectCost}

    if returnZero:
        return result
                
    # Lighting Preferences
    lux = form["luxRequirement"]

    fixtureName = form["fixtureModel"]
    fixtureBrand = form["brand"]
    fixtureLumens = form["fixtureLumens"]
    fixtureCost = form["fixtureCost"]

    fixtureData = {
        "fixtureName" : fixtureName,
        "fixtureBrand" : fixtureBrand,
        "fixtureLumens" : fixtureLumens,
        "fixtureCost" : fixtureCost,
    }

    # Verifying the provided fixture data to avoid code injection or manipulation from the front end
    if not VerifyFixtureData(fixtureData):

        AmountOfFixtures = "-"
        ProjectCost = "-"
        result = {"AmountOfFixtures" : AmountOfFixtures, 
                  "ProjectCost" : ProjectCost}

        return result

    # Casting properties that are numbers from string to actual numbers
    # to perform operations with them
    form = convertPropertiesToNumbers(form)

    # Reassigning lighting preferences
    lux = form["luxRequirement"]

    fixtureName = form["fixtureModel"]
    fixtureBrand = form["brand"]
    fixtureLumens = form["fixtureLumens"]
    fixtureCost = form["fixtureCost"]
    lightingPlaneHeight = form["lightingPlaneHeight"]

    # Floor plan shape
    fpShape = form["floorplanShape"]

    # Room dimensions
    roomLength = form["roomLength"]
    roomWidth = form["roomWidth"]
    roomHeight = form["roomHeight"]
    roomArea = form["roomArea"]

    # Room Materials
    ceilingMaterial = form["roomCeilingMaterial"]
    wallMaterial = form["roomWallMaterial"]
    floorMaterial = form["roomFloorMaterial"]

    # Checking the shape of the room
    if fpShape != "Rectangular":

        roomLength, roomWidth = math.sqrt(roomArea)
        
    # Relevant calculation data
    workplaneHeight = 0.85

    # Lumen Method calculations
    
    # Calculating the K Index
    kIndex = (roomArea) / ((lightingPlaneHeight - workplaneHeight) * (roomLength + roomWidth))

    # Getting the utilization factor based on the materials' albedo and K Index

    # Getting the albedo for each selected material
    archMaterials = Arch_Materials.query.all()

    ceilingAlbedo = list(filter(lambda x : x.name == ceilingMaterial, archMaterials))[0].albedo
    wallsAlbedo = list(filter(lambda x : x.name == wallMaterial, archMaterials))[0].albedo
    floorAlbedo = list(filter(lambda x : x.name == floorMaterial, archMaterials))[0].albedo

    # Averaging the walls' and floor's albedo
    wallsFloorAlbedo = (wallsAlbedo + floorAlbedo) / 2

    uFactor = CalculateUtilizationFactor(ceilingAlbedo, wallsFloorAlbedo, kIndex)
    maintenanceFactor = 0.8

    # Total needed luminous flux
    totalNeededLuminousFlux = (lux * roomArea) / (uFactor * maintenanceFactor)

    # OUTPUTS
    AmountOfFixtures = round(totalNeededLuminousFlux / fixtureLumens)
    ProjectCost = fixtureCost * AmountOfFixtures

    result = {"AmountOfFixtures" : AmountOfFixtures, 
              "ProjectCost" : ProjectCost}

    # Committing the new data to the Project in the DB
    WriteDataToDB(form, AmountOfFixtures, ProjectCost)

    return result


def CalculateUtilizationFactor(ceilingAlbedo, wallsFloorAlbedo, kIndex):

    # Getting the K Index selection
    try:

        for i in range(len(kIndexSelector)):

            if kIndex <= kIndexSelector[i] and kIndex < kIndexSelector[i+1]:

                selectedK = i
                break

            elif kIndex >= kIndexSelector[i] and kIndex < kIndexSelector[i+1]:

                selectedK = i
                break

    except IndexError:
        
        selectedK = -1

    if not selectedK:

        selectedK = -1

    try:

        UTableKeys = list(UTable.keys())
        for i in range(len(UTableKeys)):

            if ceilingAlbedo >= UTableKeys[i] and ceilingAlbedo > UTableKeys[i+1]:

                ceilingLevel = UTableKeys[i]
                break

            elif ceilingAlbedo <= UTableKeys[i] and ceilingAlbedo > UTableKeys[i+1]:

                ceilingLevel = UTableKeys[i]
                break

        WallsFloorsKeys = list(UTable[ceilingLevel].keys())
        for i in range(len(WallsFloorsKeys)):

            if wallsFloorAlbedo >= WallsFloorsKeys[i] and wallsFloorAlbedo > WallsFloorsKeys[i+1]:

                wallsFloorLevel = WallsFloorsKeys[i]
                break

            elif wallsFloorAlbedo <= WallsFloorsKeys[i] and wallsFloorAlbedo > WallsFloorsKeys[i+1]:

                wallsFloorLevel = WallsFloorsKeys[i]
                break

        uValue = UTable[ceilingLevel][wallsFloorLevel][selectedK]

    except IndexError:

        uValue = UTable[0.3][0.1][-1]

    return uValue

def VerifyFixtureData(fixtureData):

    modelsInDB = Models.query.all()

    matchInDB = list(filter(lambda x : fixtureData["fixtureName"] in x.name and \
                                       fixtureData["fixtureLumens"] in str(x.lm) and \
                                       fixtureData["fixtureCost"] in str(x.price) and \
                                       fixtureData["fixtureBrand"] in x.brand.name, modelsInDB))

    if matchInDB:
        return True

    else:
        return False

def WriteDataToDB(data, amountOfFixtures, projectCost):

    # Collecting relevant DB tables
    archMaterials = Arch_Materials.query.all()
    fixtureModels = Models.query.all()
    floorplansShapes = Floorplan_Shapes.query.all()

    project = Projects.query.all()
    project = list(filter(lambda x : data["projectCode"] == x.projectCode and \
                                     data["projectId"] == x.id, project))[0]

    project.roomLength = data["roomLength"]
    project.roomWidth = data["roomWidth"]
    project.roomHeight = data["roomHeight"]
    project.roomArea = data["roomArea"]
    project.roomCeilingMaterial = list(filter(lambda x : x.name == data["roomCeilingMaterial"], archMaterials))[0].id
    project.roomWallMaterial = list(filter(lambda x : x.name == data["roomWallMaterial"], archMaterials))[0].id
    project.roomFloorMaterial = list(filter(lambda x : x.name == data["roomFloorMaterial"], archMaterials))[0].id
    project.luxRequirement = data["luxRequirement"]
    project.lightingPlaneHeight = data["lightingPlaneHeight"]
    project.amountOfFixtures = amountOfFixtures
    project.totalProjectCost = projectCost
    project.dateModified = datetime.utcnow()
    project.model_id = list(filter(lambda x : x.name == data["fixtureModel"], fixtureModels))[0].id
    project.fpShape_id = list(filter(lambda x : x.name == data["floorplanShape"], floorplansShapes))[0].id
    db.session.commit()

def convertPropertiesToNumbers(form):
    # Creating a copy of the form in order to perform casting operations over its data
    copyOfForm = {}

    # Converting to numbers strings if they are numeric
    for key, value in form.items():

        if value.isnumeric():

            copyOfForm[key] = int(value)

        else:

            try:

                copyOfForm[key] = float(value)

            except ValueError:

                copyOfForm[key] = value

    return copyOfForm

def printProjectData(project):

    print("/////////////////////////////////////////////////////////////////////////////////////")
    print("id: {}".format(project.id))
    print("projectCode: {}".format(project.projectCode))
    print("name: {}".format(project.name))
    print("roomLength: {}".format(project.roomLength))
    print("roomWidth: {}".format(project.roomWidth))
    print("roomHeight: {}".format(project.roomHeight))
    print("roomArea: {}".format(project.roomArea))
    print("roomCeilingMaterial: {}".format(project.roomCeilingMaterial))
    print("roomWallMaterial: {}".format(project.roomWallMaterial))
    print("roomFloorMaterial: {}".format(project.roomFloorMaterial))
    print("luxRequirement: {}".format(project.luxRequirement))
    print("lightingPlaneHeight: {}".format(project.lightingPlaneHeight))
    print("amountOfFixtures: {}".format(project.amountOfFixtures))
    print("totalProjectCost: {}".format(project.totalProjectCost))
    print("dateModified: {}".format(project.dateModified))
    print("user_id: {}".format(project.user_id))
    print("model_id: {}".format(project.model_id))
    print("fpShape_id: {}".format(project.fpShape_id))
    print("/////////////////////////////////////////////////////////////////////////////////////")