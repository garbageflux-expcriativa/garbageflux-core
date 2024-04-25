import json

def load_registered_ids(filepath="registeredIds.json"):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {"registeredIds": []}

def save_registered_ids(data, filepath="registeredIds.json"):
    with open(filepath, 'w') as file:
        json.dump(data, file)

def add_id_to_register(new_id, filepath="registeredIds.json"):
    data = load_registered_ids(filepath)
    if new_id not in data["registeredIds"]:
        data["registeredIds"].append(new_id)
        save_registered_ids(data, filepath)
        return True
    return False

def remove_id_from_register(removal_id, filepath="registeredIds.json"):
    data = load_registered_ids(filepath)
    if removal_id in data["registeredIds"]:
        data["registeredIds"].remove(removal_id)
        save_registered_ids(data, filepath)
        return True
    return False

def is_id_registered(check_id, filepath="registeredIds.json"):
    data = load_registered_ids(filepath)
    return check_id in data["registeredIds"]

def return_ids( filepath="registeredIds.json"):
    return load_registered_ids(filepath)