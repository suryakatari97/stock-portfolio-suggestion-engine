import uuid
users = []


def user_signup(email, password, firstName, lastName):

    token = str(uuid.uuid4())

    # check if user exists
    index = next((users.index(u) for u in users if u['email'] == email), None)

    if index is not None:
        return

    users.append({'email': email, 'password': password, 'token': token, 'firstName': firstName, 'lastName': lastName})
    return token


def user_login(email, password):

    token = str(uuid.uuid4())

    # check if user exists
    index = next((users.index(u) for u in users if u['email'] == email and u['password'] == password), None)

    if index is None:
        return

    users[index]['token'] = token

    return token


def user_logout(token):

    # check if user exists
    index = next((users.index(u) for u in users if u['token'] == token), None)

    if index is None:
        return

    users[index]['token'] = None

    return


def check_login(token):

    # check if user exists
    index = next((users.index(u) for u in users if u['token'] == token), None)

    if index is None:
        return

    return users[index]
