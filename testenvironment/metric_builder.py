import json

import numpy as np
import tsgm
from sklearn.preprocessing import MinMaxScaler

import data_normalization
import loader
from analysis.anomaly_detection import build_outlier_detector
from analysis.attacker_analysis import SyntheticDataEvaluation
from analysis.compare_stats import compare_time_series
from analysis.distance_metrics import evaluate_synthetic_data
from analysis.kullback_leibler import get_kl_divergence


def run_static_tests(real_data, synthetic_data):
    """
    Run Static Tests on given real and synthetic data.

    :param real_data: A list of real data samples.
    :param synthetic_data: A list of synthetic data samples.
    :return: None
    """

    if isinstance(real_data[0], np.ndarray) and isinstance(synthetic_data[0], list):
        return evaluate_synthetic_data(build_summed_version(real_data), synthetic_data)
    else:
        base = {
            "mean_squared_error": 0,
            "wasserstein_distance": 0
        }
        for i in range(len(real_data)):
            print(type(real_data[0].shape))
            print(type(synthetic_data[0].shape))
            temp = evaluate_synthetic_data(real_data[i], synthetic_data[i])
            base["mean_squared_error"] += temp["mean_squared_error"]
            base["wasserstein_distance"] += temp["wasserstein_distance"]

        base["mean_squared_error"] = base["mean_squared_error"] / len(real_data)
        base["wasserstein_distance"] = base["wasserstein_distance"] / len(real_data)
    return base


def outlier_detection(real_data, synthetic_data):
    """
    Detect outliers in the given dataset.

    :param real_data: A list of real data samples.
    :param synthetic_data: A list of synthetic data samples.
    :return: None
    """
    if isinstance(synthetic_data[0], float):
        return build_outlier_detector(real_data, synthetic_data)
    else:
        total = [build_outlier_detector(real_data, synthetic_data[i])["total"] for i in range(len(real_data))]
        return {"total": sum(total) / len(total)}


def run_syn_analyzer_(real_data, synthetic_data):
    """
    Runs the synthetic data analyzer on the provided real and synthetic data.

    :param real_data: A list of real data samples.
    :param synthetic_data: A list of synthetic data samples.
    :return: None
    """

    real_label = np.zeros((100, 2))
    synthetic_label = np.zeros((100, 2))
    x = np.array(real_data).reshape(100, 7, 1)
    y = np.array(synthetic_data).reshape(100, 7, 1)
    real_dataset = tsgm.dataset.Dataset(x, real_label)
    synthetic_dataset = tsgm.dataset.Dataset(y, synthetic_label)
    test_dataset = tsgm.dataset.Dataset(x, real_label)

    evaluator = SyntheticDataEvaluation(real_dataset, synthetic_dataset)
    return evaluator.evaluate(test_dataset)


def run_syn_analyzer():
    """
    Runs the synthetic data analyzer.

    This method generates random data and labels and creates datasets for real data, synthetic data,
    and test data. Then, it evaluates the synthetic data using a custom evaluator.

    :return: None
    """
    size = 7
    real_data = np.random.rand(100, size, 1)
    real_label = np.random.rand(100, 2)
    synthetic_label = np.random.rand(100, 2)
    synthetic_data = np.random.rand(100, size, 1)

    real_dataset = tsgm.dataset.Dataset(real_data, real_label)
    synthetic_dataset = tsgm.dataset.Dataset(synthetic_data, synthetic_label)
    test_dataset = tsgm.dataset.Dataset(real_data, real_label)

    evaluator = SyntheticDataEvaluation(real_dataset, synthetic_dataset)
    return evaluator.evaluate(test_dataset)


def run_kullback_leibler_divergence(real_distribution, synthetic_distribution):
    """
    Calculate the Kullback-Leibler Divergence between real and synthetic distributions.

    :param real_distribution: A distribution of real data.
    :param synthetic_distribution: A distribution of synthetic data.
    :return: None
    """

    if isinstance(real_distribution[0], list) and isinstance(synthetic_distribution[0], float):
        return get_kl_divergence(build_summed_version(real_distribution), synthetic_distribution)
    else:
        total = [get_kl_divergence(real_distribution[i], synthetic_distribution[i])["kl_div"] for i in
                 range(len(real_distribution))]
    return {"kl_div": sum(total) / len(total)}


def build_data():
    x = loader.load_csv_data_as_list()
    temp = []
    scaler = MinMaxScaler()
    for i in x:
        m = i.tolist()
        m = scaler.fit_transform(np.array(m).reshape(-1, 1))
        m = [element for elements in m for element in elements]
        temp.append(m)
    process = data_normalization.PreProcessing()
    process.set_data(temp)
    return process.process()


def load_processed_data(filename="data"):
    interesting_data = {}
    with open(f"{filename}.json", "r") as json_file:
        data = json.load(json_file)
        for i in data.keys():
            if isinstance(data[i]["prediction"][0], list):
                print(len(data[i]["prediction"]))
                interesting_data[i] = np.array(data[i]["prediction"])
            else:
                interesting_data[i] = [np.array(data[i]["prediction"]) for j in range(7)]
    return interesting_data


def load_outlier(filename="test_result"):
    interesting_data = {}
    with open(f"{filename}.json", "r") as json_file:
        data = json.load(json_file)
        for i in data.keys():
            interesting_data[i] = [1 if j is True else 0 for j in data[i]["outlier"]["outliers"]]
    return interesting_data


def write_to_file(filename, all_data):
    with open(filename, "w") as json_file:
        print("writing to file ...")
        json.dump(all_data, json_file, indent=4)


def run_test_for_synthetic_data(data, syn_date_file_name, filename="test_result"):
    """
    Run a test on the provided data and synthetic data.

    :param data: The original data.
    :param syn_data: The synthetic data dictionary.

    :return: The test result dictionary.
    """
    syn_data = load_processed_data(syn_date_file_name)

    result = {}
    for i in syn_data.keys():
        result[i] = {}
        result[i]["statistic"] = run_static_tests(data, syn_data[i])
        result[i]["outlier"] = outlier_detection(data, syn_data[i])
        result[i]["attacker"] = run_syn_analyzer_(data, syn_data[i])
        result[i]["kl"] = run_kullback_leibler_divergence(data, syn_data[i])
        result[i]["numeric"] = compare_time_series(data, syn_data[i])
    write_to_file(f"{filename}.json", result)


def build_summed_version(data):
    temp = np.zeros(len(data[0]))
    for i in data:
        temp += np.array(i)
    return temp / len(data)
