import ast
import os
import json
import numpy as np


folder_path = "/stats"

file_names = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

results = {}

for file_name in file_names:
    memory_usages = []
    cpu_usages = []

    with open(os.path.join(folder_path, file_name), 'r', encoding='utf-16') as file:
        lines = file.readlines()

        for line in lines:
            try:
                stats = ast.literal_eval(line.strip())
            except (SyntaxError, ValueError):
                continue
            print(stats)
            memory_usage_str = stats['memory'].split('/')[0].strip()
            if 'GiB' in memory_usage_str:
                memory_usage = float(memory_usage_str.replace('GiB', '').strip()) * 1024  # convert GiB to MiB
            else:
                memory_usage = float(memory_usage_str.replace('MiB', '').strip())
            memory_usages.append(memory_usage)

            cpu_usage = float(stats['cpu'].replace('%', '').strip())
            cpu_usages.append(cpu_usage)

    median_memory_usage = np.median(memory_usages)
    median_cpu_usage = np.median(cpu_usages)

    results[os.path.splitext(file_name)[0]] = {
        'median_memory_usage': median_memory_usage,
        'median_cpu_usage': median_cpu_usage
    }

with open('data/results.json', 'w') as outfile:
    json.dump(results, outfile)