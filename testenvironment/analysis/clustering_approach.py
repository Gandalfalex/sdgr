import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.fftpack import fft
from scipy.signal import welch
from scipy.stats import skew, kurtosis
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, Isomap
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf
import plotly.graph_objs as go
import plotly.offline as pyo
from umap.umap_ import UMAP
from sklearn.preprocessing import LabelEncoder

def extract_features(time_series):
    time_series = np.array(time_series)

    # Basic Statistical Features
    mean = np.mean(time_series)
    std_dev = np.std(time_series)
    max_value = np.max(time_series)
    min_value = np.min(time_series)
    skewness = skew(time_series)
    kurt = kurtosis(time_series)

    # FFT Features
    fft_values = fft(time_series)
    fft_magnitudes = np.abs(fft_values)[:5]  # Using first 5 FFT coefficients

    # Autocorrelation Features (with 5 lags)
    autocorr_features = acf(time_series, nlags=5)

    # Wavelet Transform Features
    coeffs = pywt.wavedec(time_series, 'db1', level=2)  # Using Daubechies wavelet
    wavelet_features = np.hstack([coeff.ravel() for coeff in coeffs])[:5]  # Taking the first 5 features

    # Time Series Decomposition Features (Seasonal Decompose)
    # Assuming the time series has a seasonality of known period
    decomposition = seasonal_decompose(time_series, model='additive', period=12)
    trend = np.mean(decomposition.trend[~np.isnan(decomposition.trend)])
    seasonality = np.mean(decomposition.seasonal[~np.isnan(decomposition.seasonal)])
    residual = np.mean(decomposition.resid[~np.isnan(decomposition.resid)])

    # Spectral Analysis (Welch Method)
    frequencies, power = welch(time_series)
    spectral_features = power[:5]  # Taking the first 5 spectral features

    # Combine All Features
    features = np.hstack(
        [mean, std_dev, max_value, min_value, skewness, kurt, fft_magnitudes, autocorr_features, wavelet_features,
         trend, seasonality, residual, spectral_features])

    return features


def perform_clustering(all_features, k):
    all_features[np.isnan(all_features)] = 0
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(all_features)
    return kmeans.labels_, all_features


def plot_clusters(labels, features, point_labels):
    pca = PCA(n_components=3)
    reduced_features = pca.fit_transform(features)

    # Plotting in 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    scatter = ax.scatter(reduced_features[:, 0], reduced_features[:, 1], reduced_features[:, 2],
                         c=labels, cmap='viridis', marker='o')

    # Adding labels to each point
    for i, txt in enumerate(point_labels):
        ax.text(reduced_features[i, 0], reduced_features[i, 1], reduced_features[i, 2], txt, size=5, zorder=1)

    # Adding color bar for clusters
    plt.colorbar(scatter, label='Cluster Label')

    # Labelling Axes
    ax.set_xlabel('Principal Component 1')
    ax.set_ylabel('Principal Component 2')
    ax.set_zlabel('Principal Component 3')
    plt.title('3D PCA Visualization of Clustering Results with Labels')

    plt.show()


def create_plot_with_reduction(reduction_method, features, cluster_labels, categories, labels, file_name):
    reduced_features = reduction_method.fit_transform(features)

    valid_symbols = ['circle', 'circle-open', 'diamond', 'diamond-open', 'cross', 'x', 'square', 'square-open']
    le = LabelEncoder().fit(list(set(categories)))
    mapped_symbols = {class_label: valid_symbols[i % len(valid_symbols)] for i, class_label in enumerate(le.classes_)}

    traces = []
    for i, category in enumerate(set(categories)):
        category_indices = [i for i, x in enumerate(categories) if x == category]
        category_features = reduced_features[category_indices, :]
        category_labels = [labels[i] for i in category_indices]
        category_cluster_labels = [cluster_labels[i] for i in category_indices]
        if len(category_indices) == 1:
            marker_color = cluster_labels[category_indices[0]]
        else:
            marker_color = category_cluster_labels

        trace = go.Scatter3d(
            x=category_features[:, 0],
            y=category_features[:, 1],
            z=category_features[:, 2],
            mode='markers',
            marker=dict(
                size=5,
                symbol=([mapped_symbols[category]] * len(category_indices)),
                color=marker_color,
                colorscale='Viridis',
            ),
            text=category_labels,
            hoverinfo='text',
            name=category
        )
        traces.append(trace)

    layout = go.Layout(title=f'{reduction_method.__class__.__name__} Visualization for {file_name}')
    fig = go.Figure(data=traces, layout=layout)

    # Save as HTML
    pyo.plot(fig, filename=f'3d_plots/{reduction_method.__class__.__name__}_plot_{file_name}.html')


def run_cluster(real_data, syn_df, file_name="test", ml_option=True):
    print(syn_df.keys())
    syn_data = syn_df['prediction'].tolist()
    labels = syn_df['Algorithm'].tolist()


    data = real_data + syn_data
    outlier_comparison = np.random.rand(100)
    data = data + [outlier_comparison]
    original = ["original_data" for _ in range(len(real_data))]
    all_labels = original + labels + ["random_outlier"]

    k = 8
    label_dict = {}
    if ml_option:
        for label in labels:
            algorithm_name = label.split("_")[0]
            if algorithm_name in label_dict:
                label_dict[algorithm_name].append(algorithm_name)
            else:
                label_dict[algorithm_name] = [algorithm_name]
        x = list(label_dict.values())
        x = [j for i in x for j in i]
        categories = (["original"] * len(real_data) + x + ["test"])
        k = 2 + len(label_dict.keys())
    else:
        categories = ["original"] * len(real_data) + ["synthetic"] * len(syn_data) + ["test"]

    features = np.array([extract_features(ts) for ts in data])

    cluster_labels, features = perform_clustering(features, k)
    perplexity = len(all_labels) - 1
    m = [PCA(n_components=3), TSNE(n_components=3, perplexity=perplexity, n_iter=300), UMAP(n_components=3),
         Isomap(n_components=3)]
    for i in range(len(m)):
        create_plot_with_reduction(m[i], features, cluster_labels, categories, all_labels, f"{file_name}")


def create_plot_with_reduction_2d(data, labels, file_name):
    traces = []
    for arr, label in zip(data, labels):
        traces.append(
            go.Scatter(
                x=np.arange(len(arr)),
                y=arr,
                mode='lines',
                name=label  # Use corresponding label for line name
            )
        )

    # Create a layout
    layout = go.Layout(title='Line Plots of Numpy Arrays')

    # Create a figure object
    fig = go.Figure(data=traces, layout=layout)

    # Save figure as HTML
    pyo.plot(fig, filename=f'3d_plots/{file_name}_line_plots.html')


def run_2d_cluster(real_data, syn_data, labels=[], file_name="test"):
    data = real_data + syn_data
    outlier_comparison = np.random.rand(100)
    data = data + [outlier_comparison]
    original = ["original_data" for _ in range(len(real_data))]
    all_labels = original + labels + ["random_outlier"]

    create_plot_with_reduction_2d(data, all_labels, f"{file_name}")
