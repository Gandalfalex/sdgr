import json

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from survey_stats.calc_scores import calculate_tlx_score, calculate_sus_score, calculate_tlx_score_total, \
    calculate_sus_score_total
from survey_stats.plot_scores import plot_data, plot_each_result

tlx_question = ["Geistige Anforderung", "Körperliche Anforderung", "Zeitliche Anforderung", "Leistung", "Anstrengung",
                "Frustration"]
sus_question = [
    "Systemverwendung",
    "Komplexität",
    "Einfache Bedienbarkeit",
    "Unterstützung nötig",
    "Gut integriert",
    "Inkonsistent",
    "Schnelles  erlernen",
    "Umständlich zu bedienen",
    "Sicherheit im Umgang",
    "Wissen zur Betriebnahme",
]


def statistic_generator():
    """data is a list of stats"""
    with open('../data/survey_stats.json', 'r') as f:
        data = json.load(f)
    user_results = []
    all_tlx = []
    all_sus = []

    sus_data = []
    tlx_data = []
    tables = []

    for user in data:
        tlx, complete_tlx = calculate_tlx_score(fix_tlx(user["userFeeling"]))
        sus, complete_sus = calculate_sus_score(user["mentalLoad"])
        age = int(user["userInformation"]["key_personal_age"])
        affinity = int(user["userInformation"]["key_personal_technical_affinity"])
        profession = user["userInformation"].get("key_personal_background", "/")
        knowledge = user["userInformation"].get("key_personal_experience", "/")
        task = user["userInformation"].get("key_personal_task", "/")
        user_results.append({
            "tlx": tlx,
            "sus": sus,
            "age": age,
            "affinity": affinity
        })

        table = {"age": age, "affinity": affinity, "sus_score": sus, "tlx": tlx,
                 "experience": knowledge, "profession": profession, "task": task}
        all_sus.append(complete_sus)
        all_tlx.append(complete_tlx)
        tables.append(table)

    data_df = pd.DataFrame(tables)
    print(data_df.to_latex())
    plot_data(user_results)
    # test = sum_up_data(all_tlx)
    # plot_each_result(test)
    test = sum_up_data(all_sus)
    calculate_sus_score_total(all_sus)
    calculate_tlx_score_total(all_tlx)
    plot_data_as_bar_chart(test, sus_question, 5, "SUS Score")
    test = sum_up_data(all_tlx)
    plot_data_as_bar_chart(test, tlx_question, 9, "TLX Score")


def plot_data_as_bar_chart(data, questions, range, header):
    normal_value = [(sum(i) / len(i)) for i in data]
    plt.figure(figsize=(8, 5))
    plt.barh(questions, normal_value)
    plt.xlim(0, range)
    plt.title(f'{header} Verteilung')
    plt.xlabel('Punkte')
    plt.ylabel('Fragen')
    plt.show()


def sum_up_data(data):
    new_data = np.zeros((len(data[0]), len(data))).tolist()
    for i in range(len(data)):
        for j in range(len(data[i])):
            new_data[j][i] = data[i][j]
    return new_data


def fix_tlx(data):
    fixed = {}
    for i in data.keys():
        if int(i) < 7:
            fixed[i] = data[i]
    return fixed


if __name__ == "__main__":
    statistic_generator()
