import numpy as np
from scipy.stats import entropy


def get_kl_divergence(real, synthetic):
    """
    Calculate the Kullback-Leibler divergence between two probability distributions.

    :param real: An array or list representing the real distribution.
    :param synthetic: An array or list representing the synthetic distribution.
    :return: A dictionary containing the Kullback-Leibler divergence between the real and synthetic distributions.

    """
    def to_probability_distribution(data):
        hist, bin_edges = np.histogram(data, bins='auto', density=True)
        return hist / hist.sum()

    p_real = to_probability_distribution(real)
    p_synthetic = to_probability_distribution(synthetic)
    try:
        kl_div = entropy(p_real, p_synthetic)
        return {"kl_div": kl_div}
    except Exception as e:
        pass
    return {"kl_div": 0}
