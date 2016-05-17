import json

with open('/Users/henrybeggs/Desktop/Scripts/Work/file_dict') as f:
    file_dict = json.load(f)

def renumber():
    pass

for i, j in file_dict.items():
    print i, j
