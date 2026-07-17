import random
import uuid

def generate_uuid():
    return str(uuid.uuid4())

def random_bool(percent=50):
    return random.randint(1,100) <= percent

def random_price(low, high):
    return round(random.uniform(low, high),2)

def unique_sku(prefix,index):
    return f"{prefix}-{index:06d}"