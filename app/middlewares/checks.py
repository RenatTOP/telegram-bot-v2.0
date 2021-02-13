import app.database.database as db


def check_is_admin(user_id):
    isAdmin = db.check_admin(user_id)
    if (isAdmin['isAdmin'] == True):
        return True
    else:
        return False