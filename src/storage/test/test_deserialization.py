import json

line='{"name":"nasif"}'

data=json.loads(line)

print(data)
print(type(data))