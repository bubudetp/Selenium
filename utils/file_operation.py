import json

def write_to_file(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)