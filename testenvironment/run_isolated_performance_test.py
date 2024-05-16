import gc
import threading
import time

import numpy as np

import loader
from all_models_for_testing.cgan import CGAN
from all_models_for_testing.run_information import RunInformation
from memory import MemoryMonitor
from new_gans.cgan import CGANModel

modules = {
    (CGANModel, "CGAN-tsgm"),
    (CGAN, "CGAN-keras"),
}

def run_training_for_all_modules_with_iteration(data: [], name: str, input_len: int, algo: str):
    data = np.array(data)
    name = f"{name}_cgan"
    filename = f"data/{name}.json"
    all_data = loader.load_json_file(filename)
    for module, class_name in modules:
        if class_name == algo:
            data, max_l, min_l = reduce_data_specific(data, input_len)
            data = np.array(data)
            run_info = RunInformation(iterations=15, input_length=input_len)
            value = run_class_for_statistics(module, data, run_info, {})
            all_data[f"{class_name}_{input_len}"] = value
            loader.write_to_file(filename, all_data, True)


def run_class_for_statistics(module, data, run_info, data_map):
    gc.collect()
    monitor = MemoryMonitor()
    monitor_thread = threading.Thread(target=monitor.measure_memory)

    data_map = {}
    class_instance = module()
    class_instance.set_data(data)
    class_instance.set_config(run_info)

    monitor_thread.start()
    start = time.perf_counter()
    class_instance.run()
    end = time.perf_counter()
    monitor.keep_measuring = False
    monitor_thread.join()
    data_map["memory"] = monitor.max_memory

    data_map["time"] = end - start
    return data_map


def reduce_data_specific(data, test_l):
    minimum_value = np.min(data)
    maximum_value = np.max(data)
    for i in range(len(data)):
        data[i] = [(j - minimum_value) / (maximum_value - minimum_value) for j in data[i]]

    return [np.interp(np.linspace(0, len(x) - 1, test_l), np.arange(len(x)), x).tolist() for x in
            data], minimum_value, maximum_value


def run_statistics(input_length, algo_name):
    train_data_link = "data_training/output.csv"
    data = loader.load_csv_data_as_list(train_data_link)
    name = "timing_of_run_information"

    # run_training_for_all_modules(data, name, False)
    run_training_for_all_modules_with_iteration(data, name, input_length, algo_name)