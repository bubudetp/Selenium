import json
import logging

logging.basicConfig(level=logging.INFO)

def write_to_file(filename: str, data: list) -> None:
    try:
        serializable_data = json.dumps(data, default=lambda obj: list(obj) if isinstance(obj, set) else obj, indent=4)
        with open(filename, 'w') as f:
            f.write(serializable_data)
    except IOError as e:
        logging.error(f"Failed to write to file {filename}: {e}")
    except TypeError as e:
        logging.error(f"Serialization error: {e}")