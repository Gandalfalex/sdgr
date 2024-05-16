import numpy as np
import csv


def csv_to_numpy_arrays(filename="weather.csv"):
    # Use a dictionary to store the data with column names as keys
    data = {}

    with open("data/" +filename, 'r') as f:
        reader = csv.reader(f)

        # Extract the header (column names)
        header = next(reader)

        # Initialize an empty list for each column
        for column_name in header:
            data[column_name] = []

        for row in reader:
            for i, value in enumerate(row):
                if len(header[i]) == 1:
                    data[header[i]].append(float(value))

    # Convert lists to NumPy arrays
    for key in data:
        if len(data[key]) != 0:
            np.save('electricity_{}.npy'.format(key), np.array(data[key]))

    return data


# Usage:
filename = 'electricity.csv'
arrays = csv_to_numpy_arrays(filename)

