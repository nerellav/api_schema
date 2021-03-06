import yaml
## Now, validating the yaml file is straightforward:
import sys, json
import ruamel.yaml as yaml
import enum


class FileType(enum.Enum):
    JSON = 1
    YAML = 2
    XML = 3
    NOTFOUND = 4


def validateFileType(defn):
    # defn = open(defn, "r").read()
    result = FileType.NOTFOUND
    try:
        json.loads(defn)
        print("Loaded as json successfully.")
        result = FileType.JSON
    except:
        print("Unable to load as json")
        try:
            #TODO: seems to be parsing non-yaml files too fine. Need to figure out a way to raise exception
            data = yaml.safe_load(defn)
            print("Loaded as yaml successfully.")
            result = FileType.YAML
        except:
            print("Unable to load as yaml")
    print(result)
    return result


# fileType = validateFileType(r"C:\Users\vamsi\codegit\api_schema\uber.yaml")
