import json

def load_data(filePath):
  """ Loads a JSON file """
  with open(filePath, "r") as handle:
    return json.load(handle)
