import json
from pprint import pprint

with open('cs144_26s_script.json') as f:
    data = json.load(f)

# pprint(data)
print (data['results']['alternatives']['transcript'])