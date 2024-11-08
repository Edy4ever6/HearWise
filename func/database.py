from redis import Redis
import os
from dotenv import load_dotenv
from func.helpers import hash_email

# Load environment variables
load_dotenv()

# Initialize Redis
redis_db = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0))
)

def register_user(name, email, hashed_password):
    hashed_email = hash_email(email)
    redis_key = f"accounts:{hashed_email}"
    redis_db.hset(redis_key, "name", name)
    redis_db.hset(redis_key, "password", hashed_password)
    redis_db.hset(redis_key, "email", hashed_email)

def get_user_password(email):
    hashed_email = hash_email(email)
    redis_key = f"accounts:{hashed_email}"
    return redis_db.hget(redis_key, "password")

def get_user_name(email):
    hashed_email = hash_email(email)
    redis_key = f"accounts:{hashed_email}"
    return redis_db.hget(redis_key, "name").decode('utf-8')
