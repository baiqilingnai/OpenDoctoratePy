import json

def read_json(filepath: str, **args) -> dict:

    with open(filepath, **args) as f:
        return json.load(f)


def write_json(data: dict, filepath: str) -> None:

    with open(filepath, 'w') as f:
        json.dump(data, f, sort_keys=True, indent=4)

