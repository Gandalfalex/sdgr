from tsaAPI.model_generation.algorithms.amira_reconstruction import AmiraModel
from tsaAPI.model_generation.algorithms.cubic_spline import CubicSplineElement
from tsaAPI.model_generation.algorithms.emd import EmpiricalModeDecomposition
from tsaAPI.model_generation.algorithms.sarimax_model import SARIMAXModel
from tsaAPI.model_generation.algorithms.ssa import SingularSpectrumAnalysis
from tsaAPI.model_generation.algorithms.var_model import VARModel
from tsaAPI.models import TSDModel


def get_tsd_model(model: TSDModel):
    match model.pyName:
        case "EMD.py":
            return EmpiricalModeDecomposition()
        case "SSA.py":
            return SingularSpectrumAnalysis()
        case "CUBIC_SPLINE.py":
            return CubicSplineElement()
        case "AMIRA.py":
            return AmiraModel()
        case "SARIMAXModel.py":
            return SARIMAXModel()
        case "VAR.py":
            return VARModel()
        case None:
            return None
