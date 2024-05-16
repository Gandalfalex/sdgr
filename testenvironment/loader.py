import json
import os

import numpy as np
import pandas as pd


def load_csv_data_as_list(filename="data_training/weather_normalized.csv"):
    df = pd.read_csv(f"{filename}")
    data = []
    for key in df.columns:
        data.append(df[key].to_numpy())

    return data


def load_csv_data_as_dict(filename="stockdata.csv"):
    df = pd.read_csv(f"{filename}")
    data = {}
    for key in df.columns:
        data[key] = (df[key].to_numpy())

    return data


def write_data_to_csv(data, filename="new"):
    pd.DataFrame(data).T.to_csv(f"{filename}", index=False)


def load_json_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

    with open(file_path, 'r') as file:
        return json.load(file)


def create_csv_from_json(path, output_path):
    with open(path) as json_file:
        data = json.load(json_file)

    solutions = []
    headers = [h for h in data.keys()]
    for i in data.keys():
        solutions.append(data[i]['prediction'])
    pd.DataFrame(solutions).T.to_csv(output_path, index=False, header=headers)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        print(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def write_to_file(filename, all_data, increment=False):
    if increment:
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        for key in all_data.keys():
            if key in data.keys():
                data[key]['memory'] += all_data[key]['memory']
                data[key]['time'] += all_data[key]['time']
            else:
                data[key] = all_data

    with open(filename, "w") as json_file:
        json.dump(all_data, json_file, indent=4, cls=CustomEncoder)
