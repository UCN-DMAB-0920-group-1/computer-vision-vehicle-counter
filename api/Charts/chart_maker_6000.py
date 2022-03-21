import json
import numpy as np
from matplotlib import pyplot as plt
from pymongo import MongoClient
from bson.json_util import dumps

with open("api/conf.json", "r") as config:
    data = json.load(config)

client = MongoClient(data["mongodb"])
db = client['AI_result_database']
collection = db['max_distance_statistics_test']
cursor = collection.find()
list_cursor = list(cursor)
data_json = dumps(list_cursor)
x_data = []
y_data = []

for i in list_cursor:
    x_data.append(i["distance:"])
    y_data.append(i['diff'])

zero_line = [0, 0]
plt.title("100")
plt.xlabel("maximum pixel Distance")
plt.ylabel("Difference from actual count")
plt.plot(x_data, y_data, "-", marker='o')
plt.hlines(0, 0, max(x_data), colors="red", linestyles="dashed")
plt.show()
