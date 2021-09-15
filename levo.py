# importing required modules
import argparse
import requests
import json

# create a parser object
parser = argparse.ArgumentParser(description="A program to upload schemas")

# add argument
parser.add_argument("-p", "--pathspec", type=argparse.FileType('r'), help="Path to the schema file on the local "
                                                                      "filesystem.")
parser.add_argument("-a", "--application", type=str, help="Application where the schema will be uploaded to.")
parser.add_argument("-s", "--service", nargs='?', type=str, help="Service where the schema will be uploaded to.")

# parse the arguments from standard input
args = parser.parse_args()

# defining the api-endpoint
API_ENDPOINT = "http://127.0.0.1:5000/create"

# your API key here
API_KEY = "XXXXXXXXXXXXXXXXX"

schema_file = open(args.pathspec.name, "r")
application = args.application
service = args.service

defn = schema_file.read()

data = {'application': application,
        'service': service,
        'defn': defn
        }

print(data)
response = requests.post(url=API_ENDPOINT, json=data)

print (response)



