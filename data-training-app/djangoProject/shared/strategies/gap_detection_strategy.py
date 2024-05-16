from shared.preprocessing.gap_processing.imputation_algorithm import locf_imputation
from shared.preprocessing.gap_processing.imputation_algorithm import mean_imputation
from shared.preprocessing.gap_processing.imputation_algorithm import median_imputation
from shared.preprocessing.gap_processing.imputation_algorithm import nocb_imputation
from shared.preprocessing.gap_processing.imputation_algorithm import spline_interpolation


def get_imputation_algorithm_strategy(name: str):
    match name:
        case "MEDIAN":
            return median_imputation.median_imputation
        case "MEAN":
            return mean_imputation.mean_imputation
        case "NOCF":
            return nocb_imputation.nocb_imputation
        case "SPLINE INTERPOLATION":
            return spline_interpolation.spline_interpolate
        case "LOCF":
            return locf_imputation.locf_imputation
