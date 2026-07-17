from faker import Faker
import random

fake = Faker()

Faker.seed(42)

random.seed(42)

def sentence():
    return fake.sentence()

def paragraph():
    return fake.paragraph()

def company():
    return fake.company()

def date():
    return fake.date_between("+30d","+730d")

def batch():
    return fake.bothify("BAT-#####")

def warehouse():
    return random.choice([
        "Karachi Warehouse",
        "Lahore Warehouse",
        "Islamabad Warehouse",
        "Multan Warehouse",
    ])