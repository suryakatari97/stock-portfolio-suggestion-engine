import uuid
users = []


def user_signup(email, password, firstName, lastName):

    token = generateToken()

    # check if user is registered already
    registeredUser = (users.index(usr) for usr in users if usr['email'] == email)
    #print(existedUser)
    index = next(registeredUser, None)
    #print(users)
    #print("index is:", index)
    if index is not None:
        return

    users.append({'email': email, 'password': password, 'token': token, 'firstName': firstName, 'lastName': lastName})
    return token


def user_login(email, password):

    token = generateToken()

    # check if user is registered already
    registeredUser = (users.index(usr) for usr in users if usr['email'] == email and usr['password'] == password)

    index = next(registeredUser, None)

    if index is None:
        return

    users[index]['token'] = token

    return token


def user_logout(token):

    # check if user exists
    registeredUser = (users.index(usr) for usr in users if usr['token'] == token)
    index = next(registeredUser, None)

    if index is None:
        return

    users[index]['token'] = None

    return


def check_login(token):

    # check if user exists
    registeredUser = (users.index(usr) for usr in users if usr['token'] == token)
    index = next(registeredUser, None)

    if index is None:
        return

    return users[index]

def generateToken():
    return str(uuid.uuid4())
