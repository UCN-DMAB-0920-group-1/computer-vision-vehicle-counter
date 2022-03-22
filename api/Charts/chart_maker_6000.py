import json
import numpy as np
from matplotlib import pyplot as plt
from pymongo import MongoClient

with open("api/conf.json", "r") as config:
    data = json.load(config)

client = MongoClient(data["mongodb"])
db = client['AI_result_database']


def distance_plot():

    max_distance_collection = db['distance_statistics_test']
    distance_cursor = max_distance_collection.find()
    distance_list_cursor = list(distance_cursor)

    distance_collection_tokyo = db['cloudyday_distance_statistics_test']
    distance_list_cursor_tokyo = list(distance_collection_tokyo.find())

    distance_x_data = []
    distance_y_data = []
    distance_x_data_tokyo = []
    distance_y_data_tokyo = []
    distance_intercepts = []

    for i in distance_list_cursor:
        distance_x_data.append(i["value"])
        distance_y_data.append(i['diff'] * -1)
        if i['diff'] == 0:
            distance_intercepts.append(i['value'])

    print(len(distance_list_cursor_tokyo))
    for i in distance_list_cursor_tokyo:
        print(i)
        distance_x_data_tokyo.append(i["value"])
        distance_y_data_tokyo.append(i['diff'] * -1)
        if i['diff'] == 0:
            distance_intercepts.append(i['value'])

    plt.title("pixel distance analysis")

    plt.xlabel("maximum pixel Distance")
    plt.ylabel("Difference from actual count")
    plt.plot(distance_x_data, distance_y_data, "-")
    plt.plot(distance_x_data_tokyo, distance_y_data_tokyo, "-")
    for point in distance_intercepts:
        plt.plot(point, [0], marker="o", color="red")

    plt.hlines(0, 0, max(distance_x_data), colors="red", linestyles="dashed")
    plt.show()


def confidence_plot():

    confidence_collection = db['confidence_statistics_test']
    confidence_cursor = confidence_collection.find()
    confidence_list_cursor = list(confidence_cursor)

    confidence_collection_tokyo = db['cloudyday_confidence_statistics_test']
    confidence_list_cursor_tokyo = list(confidence_collection_tokyo.find())

    confidence_x_data = []
    confidence_y_data = []
    confidence_x_data_tokyo = []
    confidence_y_data_tokyo = []
    confidence_intercepts = []

    for i in confidence_list_cursor:
        confidence_x_data.append(i["value"])
        confidence_y_data.append(i['diff'] * -1)
        if i['diff'] == 0:
            confidence_intercepts.append(i['value'])

    for i in confidence_list_cursor_tokyo:
        confidence_x_data_tokyo.append(i["value"])
        confidence_y_data_tokyo.append(i["diff"] * -1)
        if i['diff'] == 0:
            confidence_intercepts.append(i['value'])

    plt.title("confidence")
    plt.xlabel("maximum pixel Distance")
    plt.ylabel("Difference from actual count")
    plt.plot(confidence_x_data, confidence_y_data, "-")
    plt.plot(confidence_x_data_tokyo, confidence_y_data_tokyo, "-")

    for point in confidence_intercepts:
        plt.plot(point, [0], marker="o", color="red")

    plt.hlines(0, 0, max(confidence_x_data), colors="red", linestyles="dashed")
    plt.show()


confidence_plot()
distance_plot()