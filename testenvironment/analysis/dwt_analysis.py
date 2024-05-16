import numpy as np
import pandas as pd
from scipy.signal import detrend, savgol_filter
from sklearn.metrics.pairwise import euclidean_distances
from dtaidistance import dtw
import matplotlib.pyplot as plt

def dwt_analysis(time_series_a, time_series_b):
    # Euclidean Distance
    scaled_a = (time_series_a - time_series_a.mean()) / time_series_a.std()
    scaled_b = (time_series_b - time_series_b.mean()) / time_series_b.std()

    # Detrending
    detrended_a = detrend(scaled_a)
    detrended_b = detrend(scaled_b)

    # Smoothing
    smoothed_a = pd.Series(detrended_a).rolling(5).mean().dropna()
    smoothed_b = pd.Series(detrended_b).rolling(5).mean().dropna()

    # Pearson Correlation
    pearson_corr = smoothed_a.corr(smoothed_b)

    # Euclidean Distance
    euc_distance = euclidean_distances([smoothed_a], [smoothed_b])[0][0]

    # Dynamic Time Warping (DTW)
    dtw_distance = dtw.distance(smoothed_a.values, smoothed_b.values)

    # Plotting results
    plt.figure(figsize=(12, 8))
    plt.subplot(3, 1, 1)
    plt.plot(smoothed_a, label='Smoothed Time Series A')
    plt.plot(smoothed_b, label='Smoothed Time Series B')
    plt.title('Smoothed Time Series')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.bar(['Pearson Correlation', 'Euclidean Distance'], [pearson_corr, euc_distance])
    plt.title('Similarity Measures')

    plt.subplot(3, 1, 3)
    plt.bar(['DTW Distance'], [dtw_distance])
    plt.title('Dynamic Time Warping Distance')

    plt.tight_layout()
    plt.show()