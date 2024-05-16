import json

import pandas as pd

import loader
elements_ml = ["data/corona_normalized_ml_result.json", "data/sinus_ml_result.json",
                              "data/electricity_new_ml_result.json", "data/output_ml_result.json", "data/weather_normalized_ml_result.json"]
elements_tsa = ["tsa/corona_normalized_tsa_result.json", "tsa/sinus_tsa_result.json",
                              "tsa/electricity_new_tsa_result.json", "tsa/output_tsa_result.json", "tsa/weather_normalized_tsa_result.json"]
all_prediction_files = ["temp/output_ml.json", "temp/sinus_ml.json", "temp/electricity_new_ml.json", "temp/corona_normalized_ml.json", "temp/weather_normalized_ml.json"]
all_prediction_files_tsa = ["tsa/output_tsa.json", "tsa/sinus_tsa.json", "tsa/electricity_new_tsa.json", "tsa/corona_normalized_tsa.json", "tsa/weather_normalized_tsa.json"]
def flatten_dict(input_dict, parent_key='', sep='.'):
    items = []
    for k, v in input_dict.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def process_data_to_dataframe(data):
    rows = []
    for entry_key, value in data.items():
        try:
            parts = entry_key.rsplit('_', 1)
            algorithm_name = parts[0]
            iteration = int(parts[1])

            flat_value = flatten_dict(value)

            row = {
                'Algorithm': algorithm_name,
                'Iteration': iteration,
            }
            row.update(flat_value)
            rows.append(row)
        except (IndexError, ValueError):
            print(f"Skipping invalid key format or value in entry: {entry_key}")
    return pd.DataFrame(rows)



def sort_json_keys(file_name):
    # Load the JSON file
    with open(file_name, 'r') as f:
        data = json.load(f)

    def get_number(key):
        parts = key.split("_")
        return int(parts[-1]) if len(parts) > 1 and parts[-1].isdigit() else 0

    # Sort keys alphabetically and numerically (if applicable)
    sorted_data = dict(sorted(data.items(), key=lambda x: (x[0].split('_')[0], get_number(x[0]))))

    # Write the sorted JSON data back to the file
    with open(file_name, 'w') as f:
        json.dump(sorted_data, f, indent=4)


def build_frame(filepaths: [], common_column="Algorithm", second_column="Iteration"):
    for i in filepaths:
        sort_json_keys(i)

    frames = []
    for i in filepaths:
        data = loader.load_json_file(i)
        frame = process_data_to_dataframe(data)
        frames.append(frame)
    if len(frames) == 1:
        return frames[0]
    combined_df = frames[0]
    for frame in range(1, len(frames)):
        combined_df = pd.merge(combined_df, frames[frame], on=[common_column, second_column])
    return combined_df


def sum_up_two_dicts(dict1, dict2):
    result = {}

    for key, value1 in dict1.items():
        value2 = dict2.get(key, None)

        if value2 is None:
            result[key] = value1
            continue

        if isinstance(value1, dict) and isinstance(value2, dict):
            result[key] = sum_up_two_dicts(value1, value2)
        elif isinstance(value1, list):
            pass
        else:
            if isinstance(value1, dict):
                sum_value = value1.get("sum", 0) + value2
                min_value = min(value1.get("min", value2), value2)
                max_value = max(value1.get("max", value2), value2)
            elif isinstance(value2, dict):
                sum_value = value1 + value2.get("sum", 0)
                min_value = min(value1, value2.get("min", value1))
                max_value = max(value1, value2.get("max", value1))
            else:
                sum_value = value1 + value2
                min_value = min(value1, value2)
                max_value = max(value1, value2)

            result[key] = {"sum": sum_value, "min": min_value, "max": max_value}
    return result

def normalize(data, value):
    for i in data.keys():
        print(i)
        if i == "loss":
            return {"-": "-"}
        if isinstance(data[i], dict) and data[i].get("sum", None) is None:
            data[i] = normalize(data[i], value)
        elif isinstance(data[i], list):
            pass
        elif data[i].get("sum", None) is not None:
            data[i]["median"] = data[i].get('sum') / value
            try:
                min_dev = ((data[i].get('min') - data[i].get('median')) / data[i].get('median')) * 100
                max_dev = ((data[i].get('max') - data[i].get('median')) / data[i].get('median')) * 100
                data[i]["deviation"] = max(abs(min_dev), abs(max_dev))
            except ZeroDivisionError:
                pass
        else:
            data[i] = data[i] / value
    return data


def open_json_file(path):
    with open(path, 'r') as file:
        data = json.load(file)
    return data


def sum_file_results(average_elements: []):
    if len(average_elements) <= 2:
        return None

    for i in average_elements:
        sort_json_keys(i)
        x = open_json_file(i)
        new_x = {}
        for j,v in x.items():
            new_j = j.replace("-", "_")
            new_x[new_j] = v
        with open(i, "w") as json_file:
            json.dump(new_x, json_file, indent=4)


    first = open_json_file(average_elements[0])
    second = open_json_file(average_elements[1])
    result = sum_up_two_dicts(first, second)
    for i in range(2, len(average_elements)):
        result = sum_up_two_dicts(result, open_json_file(average_elements[i]))
    return result


def __main__():
    files = sum_file_results(all_prediction_files)
    result = normalize(files, len(all_prediction_files))
    with open("data/timings_ml_all.json", "w") as json_file:
        json.dump(result, json_file, indent=4)


if __name__ == "__main__":
    __main__()
