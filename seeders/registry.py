SEEDERS = []

def register(cls):
    SEEDERS.append(cls())
    return cls