import numpy as np
from sklearn.ensemble import IsolationForest


def train_outlier_detector(data, contamination=0.1):
    """
    Trains an Isolation Forest model on the provided data.

    :param data: Numpy array containing the data.
    :param contamination: Estimated proportion of outliers in the data set.
    :return: Trained Isolation Forest model.
    """

    model = IsolationForest(contamination=contamination)
    for i in data:
        element = np.array(i)
        model.fit(element.reshape(-1, 1))
    return model


def detect_outliers(model, data):
    """
    Detects outliers in a numpy array using a trained model.

    :param model: Trained Isolation Forest model.
    :param data: Numpy array containing the data.
    :return: A boolean array with True for outliers and False for inliers.
    """
    predictions = model.predict(data.reshape(-1, 1))
    outliers = predictions == -1
    return outliers


def build_outlier_detector(real, synthetic):
    model = train_outlier_detector(real)
    outliers_set_2 = detect_outliers(model, synthetic)
    elements = np.zeros(real[0].shape[0])
    for i in real:
        elements += i
    elements = elements / len(real)
    outliers_set_1 = detect_outliers(model, elements)

    diffs = [True if outliers_set_1[i] == outliers_set_2[i] else False for i in range(len(outliers_set_2))]
    total = sum(1 if i is True else 0 for i in diffs)
    return {"outliers": diffs, "total": total}
