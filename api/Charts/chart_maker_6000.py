import json
import numpy as np
from matplotlib import collections, pyplot as plt
from pymongo import MongoClient

from api.src.configuration import Configuration


client = MongoClient(Configuration.get("mongodb"))
db = client['AI_result_database']


def distance_plot():
    collections = [
        "max_distance_statistics_test", "rain_night_distance_statistics_test",
        "distance_statistics_test", "cloudyday_distance_statistics_test",
        "rain_night_12_distance_statistics_test"
    ]

    distance_intercepts = []

    for collection in collections:
        dbcollection = db[collection]
        cursor = list(dbcollection.find())
        x_data = []
        y_data = []

        for i in cursor:
            x_data.append(i["value"])
            y_data.append(i['diff'] * -1)
            if i['diff'] == 0:
                distance_intercepts.append(i['value'])

        plt.plot(x_data, y_data, "-", label=collection)

    for point in distance_intercepts:
        plt.plot(point, [0], marker="o", color="red")

    plt.title("pixel distance analysis")
    plt.xlabel("maximum pixel Distance")
    plt.ylabel("Difference from actual count")
    plt.hlines(0, 0, 95, colors="red", linestyles="dashed")
    plt.legend()
    plt.show()


def confidence_plot():
    collections = [
        "confidence_statistics_test", "cloudyday_confidence_statistics_test"
    ]

    intercepts = []

    for collection in collections:
        dbcollection = db[collection]
        cursor = list(dbcollection.find())
        y_data = []
        x_data = []

        for i in cursor:
            x_data.append(i["value"])
            y_data.append(i['diff'] * -1)
            if i['diff'] == 0:
                intercepts.append(i['value'])

        plt.plot(x_data, y_data, "-", label=collection)

    for point in intercepts:
        plt.plot(point, [0], marker="o", color="red")

    plt.title("confidence analysis")
    plt.xlabel("Confidence text")
    plt.ylabel("Difference from actual count")
    plt.hlines(0, 0, 95, colors="red", linestyles="dashed")
    plt.legend()
    plt.show()


confidence_plot()
distance_plot()
