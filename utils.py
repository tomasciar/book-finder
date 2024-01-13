from fuzzywuzzy import process


def get_closest_match(user_input, data):
    highest = process.extractOne(user_input, data)
    return highest
