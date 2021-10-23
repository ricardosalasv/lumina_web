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

