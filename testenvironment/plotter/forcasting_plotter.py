import matplotlib.pyplot as plt

import loader


def plot_predictions(data, forecast_start, original):
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(18, 12))
    positions = [100, 1000, 3000, 9000]
    axes = axes.flatten()  # This will make axes a 1D array, and makes indexing easier

    for model_name, model_data in data.items():
        position = positions.index(int(model_name.split("_")[-1]))
        forecast_time = range(forecast_start, forecast_start + len(model_data['forcast']))
        ax = axes[position]  # Select the correct subplot/axis
        ax.plot(forecast_time, model_data['forcast'], label=model_name)

    for i, ax in enumerate(axes):
        ax.plot(original[0], label='original')
        ax.axvline(forecast_start, color='red', linestyle='--')
        ax.set_title(f"Forcast der Modelle mit {positions[i]} Iterationen")
        ax.set_xlabel('Zeitschritt')
        ax.set_ylabel('Wert')
        ax.legend()
        ax.grid(True)

    plt.suptitle("Forcast der Modelle auf den Corona Datensatz")
    plt.tight_layout()  # For better layout
    plt.show()


def plot_normal():
    data = loader.load_json_file("../temp/output_ml.json")
    original = loader.load_csv_data_as_list("../data_training/stockdata_normalized.csv")
    plt.plot(data["CGAN_keras_2100"]["prediction"], label='CGAN, 2100 Iterationen')
    plt.plot(data["CGAN_keras_50"]["prediction"], label='CGAN, 50 Iterationen')
    plt.plot(data["CGAN_keras_30"]["prediction"], label='CGAN, 30 Iterationen')


    plt.plot(original[0], label='Original')
    plt.title("CGAN generierte Daten gegen original Daten")

    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    data = loader.load_json_file("../data/corona_normalized_test_forcast_ml.json")
    original = loader.load_csv_data_as_list("../data_training/corona_normalized.csv")
    plot_normal()
    #plot_predictions(data, 100, "test", original)
