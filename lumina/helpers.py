import math
from lumina.models import Models
import json

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
    AmountOfFixtures = 0
    ProjectCost = 0
    result = {"AmountOfFixtures" : AmountOfFixtures, 
              "ProjectCost" : ProjectCost}

    if returnZero:
        return result

    # Outputs
    AmountOfFixtures = None
    ProjectCost = None

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

        AmountOfFixtures = 99999
        ProjectCost = 99999

        return result

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

    # Relevant calculation data
    workplaneHeight = 0.85

    # TODO
    # Lumen Calculation

def VerifyFixtureData(fixtureData):

    modelsInDB = Models.query.all()

    matchInDB = list(filter(lambda x : x.name == fixtureData["fixtureName"] and \
                                       x.price == fixtureData["fixtureCost"] and \
                                       x.lm == fixtureData["fixtureLumens"] and \
                                       x.brand == fixtureData["fixtureBrand"], modelsInDB))

    if matchInDB:
        return True

    else:
        return False

