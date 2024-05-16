import numpy as np
from scipy.stats import wasserstein_distance
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler



def evaluate_synthetic_data(real_data: np.array, synthetic_data: np.array):
    real_data = real_data.reshape(-1, 1)
    synthetic_data = synthetic_data.reshape(-1, 1)
    if real_data.shape != synthetic_data.shape:
        print(f"real:{real_data.shape} and synthetic: {synthetic_data.shape}")
        raise ValueError("Real and synthetic data must have the same shape.")

    scaler = StandardScaler()
    real_data_standardized = scaler.fit_transform(real_data)
    synthetic_data_standardized = scaler.transform(synthetic_data)

    mse = mean_squared_error(real_data_standardized, synthetic_data_standardized)

    wasserstein_dist = wasserstein_distance(real_data.ravel(), synthetic_data.ravel())

    return {
        "mean_squared_error": mse,
        "wasserstein_distance": wasserstein_dist
    }
