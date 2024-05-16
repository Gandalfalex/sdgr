import json
import os

from dataframe_builder import build_frame
from metric_builder import run_static_tests

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import loader
import argparse
from typing import Dict, List

training_files = ["data_training/weather.csv", "data_training/electricity.csv", "data_training/sinus.csv",
                  "data_training/corona_test_cases.csv", "data_training/stockdata.csv"]
normalized = ["data_training/weather_normalized.csv", "data_training/electricity_new.csv", "data_training/sinus.csv",
              "data_training/corona_normalized.csv", "data_training/output.csv"]

all_result_files = ["temp/output_ml_result.json", "temp/sinus_ml_result.json", "temp/electricity_new_ml_result.json",
                    "temp/corona_normalized_ml_result.json", "temp/weather_normalized_ml_result.json"]
all_prediction_files = ["temp/output_ml.json", "temp/sinus_ml.json", "temp/electricity_new_ml",
                        "temp/corona_normalized_ml.json", "temp/weather_normalized_ml.json"]
sinus = ["data/sinus_ml.json", "data/sinus_ml_result.json", ]
algorithms = ["CGAN-keras", "GAN", "TGAN", "TCGAN", "CGAN-tsgm", "RNN", "LSTM", "CONV_LSTM", "CNN_LSTM"]
tsa_algo = ["SSA", "EMD", "Amira", "Cubic"]


def plot_histograms(real_data, synthetic_data_dict):
    print(synthetic_data_dict.keys())

    synthetic_data = synthetic_data_dict["SSA_1"].get("prediction")
    synthetic_data = np.array(synthetic_data)
    real_data = np.array(real_data)

    best_values = []
    for i in range(len(real_data)):
        for j in range(len(synthetic_data)):
            val = run_static_tests(real_data[i], synthetic_data[j])
            best_values.append(val['mean_squared_error'])

    print(best_values)
    syn_organized = []
    for i in range(len(real_data)):
        pos = i * len(synthetic_data)
        temp = best_values[pos: pos + len(synthetic_data)]
        best_syn_match = min(temp)
        real_index = temp.index(best_syn_match)
        syn_organized.append(synthetic_data[real_index])
        print(f"i: {i} with distance: {real_index % len(synthetic_data)} with value: {best_syn_match}")

    syn_organized = np.array(syn_organized)

    fig, axs = plt.subplots(2, 3, figsize=(12, 8))
    fig.suptitle('Originale and Synthetische Datenverteilung', fontsize=16)

    for i in range(6):
        sns.histplot(syn_organized[i], bins=50, alpha=0.5, label='Synthetische Daten',
                     ax=axs[i % 2, i % 3], color='blue')
        sns.histplot(real_data[i], bins=50, alpha=0.5, label='Originale Daten', ax=axs[i % 2, i % 3],
                     color='orange')
        axs[i % 2, i % 3].set_title(f'Datensatz {i}', fontsize=12)
        axs[i % 2, i % 3].set_xlabel('Werte')
        axs[i % 2, i % 3].set_ylabel('Frequenz')
        axs[i % 2, i % 3].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

    # Create a 2x3 grid of subplots
    fig, axs = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Originale and Synthetische Datenverteilung', fontsize=16)

    for i in range(6):
        sns.scatterplot(real_data[i], label='Real Data', alpha=0.5,
                        ax=axs[i % 2, i % 3])
        sns.scatterplot(syn_organized[i],
                        label='Generated Data', alpha=0.5, ax=axs[i % 2, i % 3])
        axs[i % 2, i % 3].set_title(f'Element {i}', fontsize=12)
        axs[i % 2, i % 3].set_xlabel('Zeitwerte')
        axs[i % 2, i % 3].set_ylabel('Stärke')
        axs[i % 2, i % 3].legend()

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def plot_data_2d(df, x_col, x_label, y_col, y_label, file="", use_only=["RNN", "LSTM", "CONV_LSTM", "CNN_LSTM"]):
    plt.figure(figsize=(12, 8))
    for algorithm in df[df['Algorithm'].isin(use_only)]['Algorithm'].unique():
        subset = df[df['Algorithm'] == algorithm]
        # subset = subset[subset[x_col] <= 500]
        plt.plot(subset[x_col], subset[y_col], label=algorithm)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(f"{x_label} gegen {y_label}")
    plt.legend()
    plt.grid(True)
    plt.savefig(f'images/{x_col}_{y_col}{file}.png')
    plt.show()


def analyze_algorithm(algorithm_data, algorithm_name, label="Iteration"):
    # Creating DataFrame
    df = algorithm_data[algorithm_data['Algorithm'] == algorithm_name]
    print(df.keys())
    # df.to_csv(f'images/{algorithm_name}_data.csv')
    # Plotting
    fig, ax = plt.subplots(2, 3, figsize=(16, 12))
    fig.suptitle(f'Analyse für {algorithm_name}', fontsize=16)

    # KL divergence plot
    ax[0, 0].plot(df[label], df['statistic.wasserstein_distance.median'], marker='o', color='b',
                  label='Wasserstein Distanz')
    ax[0, 0].set_xlabel('Iteration')
    ax[0, 0].set_ylabel('Wasserstein Distanz')
    ax[0, 0].legend()
    ax[0, 0].grid(True)

    # Attacker privacy plot
    ax[0, 1].plot(df[label], df['numeric.std_dev_diff.median'], marker='o', color='g', label='Standardabweichung')
    ax[0, 1].set_xlabel('Iteration')
    ax[0, 1].set_ylabel('Abweichung')
    ax[0, 1].legend()
    ax[0, 1].grid(True)

    ax[0, 2].plot(df[label], df['numeric.mann_whitney_u_stat.median'], marker='o', color='r',
                  label='Mann Whitney U Test')
    ax[0, 2].set_xlabel('Iteration')
    ax[0, 2].set_ylabel('U Wert des Mann Whitney U Tests')
    ax[0, 2].legend()
    ax[0, 2].grid(True)

    # Attacker privacy plot
    ax[1, 0].plot(df[label], df['attacker.similarity.median'], marker='o', color='orange', label='Vektordistanz')
    ax[1, 0].set_xlabel('Iteration')
    ax[1, 0].set_ylabel('Vektordistanz')
    ax[1, 0].legend()
    ax[1, 0].grid(True)

    # Attacker privacy plot
    ax[1, 1].plot(df[label], df['attacker.privacy.median'], marker='o', color='purple',
                  label='Privatsphäre durch Membership Interference Attack')
    ax[1, 1].set_xlabel('Iteration')
    ax[1, 1].set_ylabel('MIA Wert')
    ax[1, 1].legend()
    ax[1, 1].grid(True)

    ax[1, 2].plot(df[label], df['numeric.mann_whitney_u_p_val.median'], marker='o', color='y',
                  label='Mann Whitney U Test')
    ax[1, 2].set_xlabel('Iteration')
    ax[1, 2].set_ylabel('P Wert des Mann Whitney U Tests')
    ax[1, 2].legend()
    ax[1, 2].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(f'images/{algorithm_name}_analysis.png')
    plt.show()

    # Saving DataFrame to CSV
    # df.to_csv(f'images/{algorithm_name}_data.csv')


def plot_data_zoomed(df, x_col, x_label, y_col, y_label, title, name="test.png"):
    fig, ax = plt.subplots(figsize=(12, 8))
    for algorithm in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algorithm]
        ax.plot(subset[x_col], subset[y_col], label=algorithm)

    x1, x2, y1, y2 = 0, 2150, 1, 350
    axins = ax.inset_axes([0.59, 0.1, 0.4, 0.3])
    for algorithm in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algorithm]
        axins.plot(subset[x_col], subset[y_col], label=algorithm)
        axins.grid(True)

    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    ax.indicate_inset_zoom(axins, lw=1, edgecolor="red")

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend(loc="upper left")
    ax.grid(True)
    plt.savefig(f'images/{name}.png')
    plt.show()


def plot_changes_3d(df, xkey, ykey, zkey, name):
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    for algorithm in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algorithm]
        subset = subset[subset["training-time"] <= 200]

        ax.plot(subset[xkey], subset[ykey], subset[zkey], label=algorithm)

    x_name = xkey.split(".")[1] if xkey.count(".") == 1 else xkey
    y_name = ykey.split(".")[1] if ykey.count(".") == 1 else ykey
    z_name = zkey.split(".")[1] if zkey.count(".") == 1 else zkey

    ax.set_xlabel(x_name)
    ax.set_ylabel(y_name)
    ax.set_zlabel(z_name)
    plt.title('Abhängigkeit der Wasserstein Distanze zur privatsphäre Metrik über Iterationen')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'images/{name}.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_training_data(files: [], training: []):
    for i in range(len(files)):
        name = files[i].split(".")[0].split("/")[1]
        plt.figure(figsize=(16, 6))
        data = loader.load_csv_data_as_dict(files[i])
        train = loader.load_csv_data_as_dict(training[i])
        for k in train.keys():
            plt.plot(data[k], label=k)
        plt.legend()
        plt.grid(True)
        plt.savefig(f'images/{name}.png', dpi=300, bbox_inches='tight')


def plot_iteration_change(frame, algo):
    subset = frame[frame['Algorithm'] == "RNN"]
    if isinstance(subset['prediction'].iloc[0], str):
        import ast
        subset['prediction'] = subset['prediction'].apply(ast.literal_eval)

    fig, ax = plt.subplots(figsize=(10, 7))  # or whatever size you want

    # Plot each list
    for idx, prediction in enumerate(subset['prediction']):
        if (idx % 2 == 0):
            ax.plot(prediction, label=f'Series {idx}')

    ax.set_xlabel('Index')
    ax.set_ylabel('Value')

    # Add this if you want a legend
    plt.legend()

    plt.show()


def range_display(frames, plot=True):
    df_concat = pd.concat(frames)

    attributes = ['statistic.mean_squared_error', 'statistic.wasserstein_distance',
                  'outlier.total', 'attacker.similarity', 'attacker.consistency',
                  'attacker.downstream', 'attacker.privacy', 'kl.kl_div',
                  'numeric.mean_diff', 'numeric.median_diff', 'numeric.std_dev_diff',
                  'numeric.autocorrelation', 'numeric.t_test_stat', 'numeric.t_test_p_val',
                  'numeric.mann_whitney_u_stat', 'numeric.mann_whitney_u_p_val']

    # For each important column calculate min, med, and max
    aggregation = {col: ['min', 'median', 'max'] for col in attributes}

    df_agg = df_concat.groupby(['Algorithm', 'Iteration']).agg(aggregation)

    # Flattening MultiIndex columns
    df_agg.columns = ['_'.join(col).strip() for col in df_agg.columns.values]

    df_agg.reset_index(inplace=True)

    if plot:
        for algorithm in df_agg['Algorithm'].unique():
            df_alg = df_agg[df_agg['Algorithm'] == algorithm]

            for attribute in attributes:
                plt.figure(figsize=(10, 5))
                lower_bound = df_alg[f'{attribute}_min'].values
                max_lower_bound = lower_bound + 0.3 * df_alg[f'{attribute}_median'].values
                upper_bound = df_alg[f'{attribute}_max'].values
                min_upper_bound = upper_bound - 0.3 * df_alg[f'{attribute}_median'].values
                median = df_alg[f'{attribute}_median'].values
                t = df_alg['Iteration'].values

                plt.plot(t, median, lw=2, label='Median')
                plt.fill_between(t, lower_bound, upper_bound, facecolor='C0',
                                 alpha=0.4, label='Abweichung vom Median, Maxima und Minima')

                attribute_name = attribute.split(".")[1].replace("_", " ")
                attribute_name = attribute_name.capitalize()
                plt.xlabel('Iteration')
                plt.ylabel(attribute_name)
                plt.title(f'Algorithmus: {algorithm}, Veränderung von {attribute_name} über Iterationen')
                plt.legend()
                plt.grid(True)
                plt.savefig(f'graph_image/{attribute}-{algorithm}.png')
                plt.close()
    else:
        pct_change_cols = []
        for attribute in attributes:
            for stat in ['min', 'median', 'max']:
                df_agg[f'{attribute}_{stat}_pct_change'] = (
                        df_agg.groupby('Algorithm')[f'{attribute}_{stat}'].pct_change() * 100)
                pct_change_cols.append(f'{attribute}_{stat}_pct_change')

        # Display change percentages
        print(df_agg[['Algorithm', 'Iteration',
                      'attacker.privacy_median_pct_change',
                      'statistic.wasserstein_distance_median_pct_change',
                      'attacker.similarity_median_pct_change']].to_latex(index=False))


def main(data: Dict[str, str]):
    df = build_frame(data['filenames'])
    if data['operation'] == 'plot_histograms':
        plot_histograms(data['real_data'], data['synthetic_data_dict'])
    elif data['operation'] == 'plot_data_2d':
        plot_data_2d(df, data['x_col'], data['x_label'], data['y_col'], data['y_label'], data['file'], data['use_only'])
    elif data['operation'] == 'analyze_algorithm':
        analyze_algorithm(data['algorithm_data'], data['algorithm_name'], data['label'])
    elif data['operation'] == 'plot_data_zoomed':
        plot_data_zoomed(df, data['x_col'], data['x_label'], data['y_col'], data['y_label'], data['title'],
                         data['name'])
    elif data['operation'] == 'plot_changes_3d':
        plot_changes_3d(df, data['xkey'], data['ykey'], data['zkey'], data['name'])
    elif data['operation'] == 'plot_training_data':
        plot_training_data(data['files'], data['training'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Various plotting operations')
    subparsers = parser.add_subparsers(dest="operation")

    parser_histograms = subparsers.add_parser('plot_histograms')
    parser_histograms.add_argument('--real_data', dest='real_data_histograms', type=str, required=True)
    parser_histograms.add_argument('--synthetic_data', dest='synthetic_data_histograms', type=str, required=True)

    parser_data_2d = subparsers.add_parser('plot_data_2d')
    parser_data_2d.add_argument('--files', nargs='+', help='List of training data csv files', dest='df_data_2d', type=str, required=True)
    parser_data_2d.add_argument('--x_col', dest='x_col_data_2d', type=str, required=True)
    parser_data_2d.add_argument('--x_label', dest='x_label_data_2d', type=str, required=True)
    parser_data_2d.add_argument('--y_col', dest='y_col_data_2d', type=str, required=True)
    parser_data_2d.add_argument('--y_label', dest='y_label_data_2d', type=str, required=True)
    parser_data_2d.add_argument('--file', dest='file_data_2d', type=str, required=False)
    parser_data_2d.add_argument('--use_only', dest='use_only_data_2d', type=list, required=False)

    args = parser.parse_args()

    args_dict = vars(args)
    main(args_dict)
