from passlib.context import CryptContext

pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")

def hash_p(password: str):
    return pwd_context.hash(password)

def verify(plain_pwd,hash_pwd):
    return pwd_context.verify(plain_pwd,hash_pwd)