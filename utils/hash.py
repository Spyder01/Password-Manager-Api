from bcrypt import hashpw, checkpw, gensalt


def hash_password (password):
    return hashpw(password, gensalt(12))

def check_password (password, database_password):
    return checkpw(password, database_password)


def user_hash_username (email, password):
    return hashpw(email+password, gensalt(12))
