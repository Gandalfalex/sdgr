import argparse
import time

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

import data_normalization
import loader
from all_models_for_testing.CNNLSTM import CNN_LSTM
from all_models_for_testing.CONVLstm import CONVLstm
from all_models_for_testing.amira_imp import AmiraModel
from all_models_for_testing.cgan import CGAN
from all_models_for_testing.cubic import CubicSplineElement
from all_models_for_testing.emd import EmpiricalModeDecomposition
from all_models_for_testing.gan import GAN
from all_models_for_testing.ltsm import LSTM_custom
from all_models_for_testing.rnn import RNN
from all_models_for_testing.run_information import RunInformation
from all_models_for_testing.ssa import SingularSpectrumAnalysis
from analysis.clustering_approach import run_cluster
from dataframe_builder import build_frame
from metric_builder import run_test_for_synthetic_data
from new_gans.cgan import CGANModel
from new_gans.tcgan import TCGANModel
from new_gans.tgan import TGANModel
from run_isolated_performance_test import run_statistics

training_data_csv = [
    "data_training/corona_normalized.csv", "data_training/electricity_new.csv",
    "data_training/stockdata_normalized.csv",
    "data_training/sinus.csv", "data_training/weather_normalized.csv"
]

modules = [
    # (RCGANModel, "RCGAN"),
    (TGANModel, "TGAN"),
    (TCGANModel, "TCGAN"),
    (CGANModel, "CGAN-tsgm"),
    (CGAN, "CGAN-keras"),
    (GAN, "GAN"),
    (LSTM_custom, "LSTM"),
    (RNN, "RNN"),
    (CNN_LSTM, "CNN_LSTM"),
    (CONVLstm, "CONV_LSTM")
]

tsa_modules = [
    (AmiraModel, "Amira"),
    (CubicSplineElement, "Cubic"),
    (EmpiricalModeDecomposition, "EMD"),
    (SingularSpectrumAnalysis, "SSA"),
]


def run_training_for_all_modules(train_data_path, name: str, use_ml=True, use_forcast=False):
    data = loader.load_csv_data_as_list(train_data_path)
    test, _, _ = reduce_data(data)
    # iterations = [30,50,70,100,140,210,300,500,700,1400,2100]
    iterations = [100, 1000, 3000, 9000]

    data = np.array(test)
    name = f"{name}_{'ml' if use_ml else 'tsa'}"
    filename = f"{'data' if use_ml else 'tsa'}/{name}.json"
    print(filename)
    all_data = loader.load_json_file(filename)

    if use_ml:
        for module, class_name in modules:
            for iteration in iterations:
                if class_name == "RNN" or class_name.count("LSTM") == 1:
                    run_info = RunInformation(iterations=int(iteration / len(data)), input_length=100,
                                              forcast=use_forcast)
                else:
                    run_info = RunInformation(iterations=iteration, input_length=100, forcast=use_forcast)
                value = run_class(module, class_name, data, run_info, {})
                all_data[f"{class_name}_{iteration}"] = value
                loader.write_to_file(filename, all_data)
    else:
        for module, class_name in tsa_modules:
            if class_name == "EMD" or class_name == "SSA":
                for i in range(6):
                    run_info = RunInformation(iterations=0, input_length=100, precision=i, forcast=use_forcast)
                    value = run_class(module, class_name, data, run_info, {})
                    all_data[f"{class_name}_{i}"] = value
            else:
                run_info = RunInformation(iterations=0, input_length=100, forcast=use_forcast)
                value = run_class(module, class_name, data, run_info, {})
                all_data[f"{class_name}_{1}"] = value
            loader.write_to_file(filename, all_data)


def run_class(module, class_name, data, run_info, data_map):
    data_map = {}
    try:
        class_instance = module()
        class_instance.set_data(data)
        class_instance.set_config(run_info)
        start = time.perf_counter()
        info = class_instance.run()
        end = time.perf_counter()
        data_map["training-time"] = end - start
        data_map["prediction"] = info.get_prediction()
        data_map["prediction"] = info.get_prediction()
        data_map["forcast"] = info.get_forcast()
        data_map["other"] = info.as_dict()

    except Exception as e:
        data_map["errors"] = f"error with {class_name}: {str(e)}"
    return data_map


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


def save_normalized_data(data):
    x, _, _ = reduce_data(data)

    df = pd.DataFrame(x).T
    df.to_csv('weather_normal_1.csv', index=False, header=False)


def build_cluster(data, file_names, trainig_name=""):
    frame = build_frame(file_names)
    isMl = trainig_name.count("ml") > 0
    run_cluster(data, frame, trainig_name, isMl)


def reduce_data(data):
    minimum_value = np.min(data)
    maximum_value = np.max(data)
    for i in range(len(data)):
        data[i] = [(j - minimum_value) / (maximum_value - minimum_value) for j in data[i]]

    return [np.interp(np.linspace(0, len(x) - 1, 100), np.arange(len(x)), x).tolist() for x in
            data], minimum_value, maximum_value


def reduce_data_specific(data, test_l):
    minimum_value = np.min(data)
    maximum_value = np.max(data)
    for i in range(len(data)):
        data[i] = [(j - minimum_value) / (maximum_value - minimum_value) for j in data[i]]

    return [np.interp(np.linspace(0, len(x) - 1, test_l), np.arange(len(x)), x).tolist() for x in
            data], minimum_value, maximum_value


def inflate_data(data, minimum_value, maximum_value, length):
    data = [(j * (maximum_value - minimum_value) + minimum_value) for j in data]
    return interpolate_original_length(data, length)


def interpolate_original_length(data, original_l):
    return np.interp(np.linspace(0, len(data) - 1, original_l), np.arange(len(data)), data)


def __main__(training_data_csv, use_ml):
    for i in training_data_csv:
        name = i.split("/")[1].split(".")[0]
        data = loader.load_csv_data_as_list(i)
        test, _, _ = reduce_data(data)
        work_data = np.array(test)
        run_training_for_all_modules(i, name, use_ml)
        path = f"ml/{name}_ml" if use_ml else f"tsa/{name}_tsa"
        run_test_for_synthetic_data(work_data, path, path + "_result")
        build_cluster(test, [path], path + "_testing")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Your app description here')
    parser.add_argument('-f', '--files', nargs='+', help='List of training data csv files')
    parser.add_argument('-m', '--use_ml', type=bool, default=False, help='Use ML')

    # Create mutually exclusive group for input_length and algo_name
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--input_length', type=int, help='Input length for statistics')
    group.add_argument('-a', '--algo_name', type=str, help='Algorithm name for statistics')

    args = parser.parse_args()
    print(args)

    if args.input_length and args.algo_name:
        print(f"new start with {args.input_length} and {args.algo_name}")
        run_statistics(args.input_length, args.algo_name)
    elif args.files:
        __main__(args.files, args.use_ml)
    else:
        parser.error('No arguments provided.')
