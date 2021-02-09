import database


users = database.db.users

def chek_admin(user_id):
    isAdmin = users.find_one({"userId": user_id}, {'isAdmin': True})
    if (isAdmin['isAdmin'] == True):
        return True
    else:
        return False
    