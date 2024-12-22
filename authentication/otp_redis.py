import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)

def store_otp(phone_number, otp, ttl=300):
    redis_client.setex(f"otp:{phone_number}", ttl, otp)

def retrieve_otp(phone_number):
    return redis_client.get(f"otp:{phone_number}")

def delete_otp(phone_number):
    redis_client.delete(f"otp:{phone_number}")
