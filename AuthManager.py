import hashlib
import item
import DBManager as db
from fastapi_login.exceptions import InvalidCredentialsException

class Status:
    success = "success"
    fail = "fail"


async def login(user: item.loginItem):
    dbUser = await db.getAdmin(user=user.user)
    hashPassword = hashlib.md5(user.password.encode())
    
    if hashPassword.hexdigest() != dbUser['password']:
        raise InvalidCredentialsException
    else:
        return user.user

