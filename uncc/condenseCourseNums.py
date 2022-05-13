import json

data = []

with open("pages.json", "r") as f:
    data = json.loads(f.read())


courseNumbers = []

for line in data:
    for num in line['response']:
        courseNumbers.append(num)

with open("courseNumbers.txt", "w") as f:
    for num in courseNumbers:
        f.write(num + ",")
