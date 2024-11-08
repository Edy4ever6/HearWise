import hashlib
import bcrypt

def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
