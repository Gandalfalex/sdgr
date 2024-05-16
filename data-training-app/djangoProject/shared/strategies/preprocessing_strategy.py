from shared.models import PreprocessorType
from shared.preprocessing.data_formatting.default_processing import DefaultPreprocessing
from shared.preprocessing.data_formatting.remove_linear_trend import LinearTrendProcessing
from shared.preprocessing.data_formatting.simple_reduction import SimpleReductionPreprocessing


def get_preprocessor_strategy(processor_type: PreprocessorType):
    match processor_type.name:
        case "LinearTrendRemove":
            return LinearTrendProcessing()
        case "SimpleReduction":
            return SimpleReductionPreprocessing()
        case None:
            return DefaultPreprocessing()
