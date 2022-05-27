# File: tools.py
import json


def check_credit_card_number(card_number):
    if type(card_number) != str \
            or len(card_number) != 16:  # Card number should be
        return False                    # a string of 16 digits
    try:
        int(card_number)                # Card number should be num only
    except:
        return False

    return True  # good data


# R1. Get JSON file data
def read_JSON_from_txt(file):
    with open(file, 'r') as openfile:   # open file
        return json.load(openfile)      # Get Json from file


# R1. Write JSON to file
def write_JSON_to_txt(file, items):
    json_object = json.dumps(items, indent=4)  # Serializing JSON

    with open(file, "w") as outfile:    # open file
        outfile.write(json_object)      # write JSON to file
