import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
jwt_secret_key = os.getenv('JWT_SECRET_KEY')

def create_jwt_token(email, name):
    return jwt.encode(
        {
            "email": email,
            "name": name,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=600)
        },
        jwt_secret_key,
        algorithm="HS256"
    )

def decode_jwt_token(token):
    try:
        return jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}
