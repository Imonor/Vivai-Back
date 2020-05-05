"""File to automatically fill the DB"""

from json import load

import common.db_dealer as db_dealer

JSON_FILE = "common/plant_pair.json"

def fill_supported_plants():
    """Fills the SupportedPlant table"""
    generator = yield_json(JSON_FILE)

    for _ in range(3):
        plants_to_add = []
        try:
            for _ in range(25):
                plants_to_add.append(next(generator))
            db_dealer.insert_supported_plants(plants_to_add)

        except StopIteration:
            db_dealer.insert_supported_plants(plants_to_add)
            break

def yield_json(file):
    """Yields elements of the json file"""
    with open(file, 'r') as f:
        for item in load(f):
            yield item
