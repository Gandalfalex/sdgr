---
title: "Testing Process"
date: 2023-12-08T19:22:33+01:00
tags: [docker, django, start]
featured_image: ""
description: "Guide to run the tests"
---

## Prerequisites

- Docker and Docker Compose installed.
- Python 3.11 environment for Django.




#### Creating a Virtual Environment

Before setting up your Testing framework, it's recommended to create a virtual environment. This ensures that your project's dependencies are isolated from the global Python environment.

1. **Navigate to your project directory:**
```bash
cd testenvironment
```
2. **Create the virtual environment:**

For Windows:
```bash
python -m venv venv
```
For macOS and Linux:
```bash
python3 -m venv venv
```

3. **Activate the virtual environment:**

For Windows:
```bash
.\venv\Scripts\activate
```
For macOS and Linux:
```bash
source venv/bin/activate
```

4. **Install the required packages:**

For Windows:
```bash
pip install -r requirements.txt
```
For macOS and Linux:
```bash
pip3 install -r requirements.txt
```


# Testing
## Start the Docker Test
For Performance Measurements, the testenvironment starts up a docker container and runs a predifined command.
This is all one through one powershell script. This only works on windows


Simply run
````bash
isolation_testing.ps1
````


## Normal test

The script accepts several command-line arguments to control its behavior:

- `-f` or `--files`: Accepts one or more paths to training data CSV files.
- `-m` or `--use_ml`: A boolean flag to indicate whether to use Machine Learning (ML) methods.
- `-i` or `--input_length`: Specifies the input length for statistical methods.
- `-a` or `--algo_name`: Specifies the name of the algorithm to be used in statistical methods.

### Examples

1. **Running the Test for ML**:
```bash
python main.py -f "data1.csv" "data2.csv" -m True
```

2. **Running the Test for TSA**:
```bash
python main.py -f "data1.csv" "data2.csv" -m False
```

## Creating images
### Operations
The script supports the following operations:
 plot_histograms
 plot_data_2d

### plot_histograms
```bash
python plot_statistics_from_json.py plot_histograms --real_data real_data_value --synthetic_data synthetic_data_value
```

- `--real_data`: The real_data parameter for the plot_histograms operation
- `--synthetic_data`: The synthetic_data parameter for the plot_histograms operation

### plot_data_2d
```bash
python plot_statistics_from_json.py plot_data_2d -f data/sinus_ml_result.json + data/weather_ml_result.json --x_col x_col_value --x_label x_label_value --y_col y_col_value --y_label y_label_value --file file_value --use_only 'RNN'
```

- `-f` or `--files`: L
- `--x_col`: The x_col parameter for the plot_data_2d operation
- `--x_label`: The x_label parameter for the plot_data_2d operation
- `--y_col`: The y_col parameter for the plot_data_2d operation
- `--y_labe`l: The y_label parameter for the plot_data_2d operation
- `--file`: (Optional) The file parameter for the plot_data_2d operation
- `--use_only`: (Optional) The use_only parameter for the plot_data_2d operation