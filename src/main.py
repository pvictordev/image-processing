import os
import json
from image_processing import process_image

def batch_process(config_path):
    """Loads the config file and processes multiple images."""
    with open(config_path, 'r') as file:
        config = json.load(file)

    images = config["images"]
    operations = config["operations"]
    output_directory = config["output_directory"]

    os.makedirs(output_directory, exist_ok=True)

    for image_path in images:
        process_image(image_path, operations, output_directory)

if __name__ == "__main__":
    batch_process("config.json")
