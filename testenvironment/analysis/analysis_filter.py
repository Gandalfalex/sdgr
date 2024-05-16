from pykalman import KalmanFilter
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from statsmodels.nonparametric.kernel_regression import KernelReg
from scipy.signal import butter, lfilter


# Lowpass filter11
def exponential_smoothing(data, alpha=0.01):
    smoothed_data = np.zeros_like(data)
    smoothed_data[0] = data[0]

    for i in range(1, len(data)):
        smoothed_data[i] = alpha * data[i] + (1 - alpha) * smoothed_data[i - 1]

    return smoothed_data


def kernel_filter(data, bandwidth):
    # Ajustar el modelo de regresión con kernel
    kr = KernelReg(endog=data, exog=np.arange(len(data)), var_type='c', reg_type='lc', bw=[bandwidth])
    mean, _ = kr.fit(np.arange(len(data)))
    return mean


# highpass filter
def sobel_filter(data):
    # Sobel Kernel para una dimensión
    kernel = np.array([-1, 0, 1])
    return np.convolve(data, kernel, mode='same')


def butterworth_filter(data, order=2, cutoff_freq=0.25):
    # Diseño del filtro IIR pasa altas usando Butterworth
    b, a = butter(order, cutoff_freq, btype='high', analog=False)
    return lfilter(b, a, data)


def normalize_array(arr):
    min_val = np.min(arr)
    max_val = np.max(arr)
    normalized_arr = (arr - min_val) / (max_val - min_val)
    return normalized_arr


def get_similiarity(a, b):
    common_outliers = []
    for element_a in a:
        for element_b in b:
            if abs(element_a - element_b) <= threshold:
                common_outliers.append((element_a, element_b))
    return common_outliers


if __name__ == '__main__':
    data = np.load("data/weather_VPact (mbar).npy")
    data = normalize_array(data[0])
    model = LocalOutlierFactor(n_neighbors=20, contamination=0.05)

    plt.plot(data, label='Weather')
    plt.plot(kernel_filter(data, 10), label='Kernel')
    plt.plot(exponential_smoothing(data), label='Kalman')
    plt.plot(sobel_filter(data), label='Sobel')
    plt.plot(butterworth_filter(data, 10), label='Butterworth')

    outlier_scores = model.fit_predict(data.reshape(-1, 1))
    outlier_indices = np.where(outlier_scores == -1)[0]
    plt.scatter(outlier_indices, data[outlier_indices], color='red', label='Outliers')

    plt.legend()
    plt.show()
