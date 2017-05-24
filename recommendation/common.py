import json

def print_dict(value):
    print json.dumps(value, indent = 4, sort_keys = True)

def extract_keys(*args):
    keys = set()
    for value in args:
        for key in value:
            keys.add(key)

    return keys



