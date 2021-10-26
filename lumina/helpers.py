import math

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

def CalculateProject(form):

    """
    Lighting calculation based on the Lumen method
    """

    # Outputs
    AmountOfFixtures = None
    ProjectCost = None

    # Lighting Preferences
    lux = form.luxRequirement.data

    fixtureName = form.fixtureModel.data
    fixtureBrand = form.brand.data
    fixtureLumens = form.fixtureLumens.data
    fixtureCost = form.fixtureCost.data

    fixtureData = [
        fixtureName,
        fixtureBrand,
        fixtureLumens,
        fixtureCost
    ]

    # Verifying the provided fixture data to avoid code injection or manipulation from the front end
    if not VerifyFixtureData(fixtureData):

        AmountOfFixtures = 99999
        ProjectCost = 99999

        return [AmountOfFixtures, ProjectCost]

    # Floor plan shape
    fpShape = form.floorplanShape.data

    # Room dimensions
    roomLength = form.roomHeight.data
    roomWidth = form.roomHeight.data
    roomHeight = form.roomHeight.data
    roomArea = form.roomHeight.data

    # Room Materials
    ceilingMaterial = form.roomCeilingMaterial.data
    wallMaterial = form.roomWallMaterial.data
    floorMaterial = form.roomFloorMaterial.data

    # Relevant calculation data
    workplaneHeight = 0.85

    # TODO
    # Lumen Calculation

def VerifyFixtureData(fixtureData):

    # TODO
    # Verify fixture data against data in the DB
    pass

