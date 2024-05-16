import {JsonSchema7} from "@jsonforms/core";
import {CalculationMethod} from "../spring_types";

const numericSchema: JsonSchema7 = {
    "properties": {
        "name": {
            "type": "string",
            "description": "The name of the data set."
        },
        "numSamples": {
            "type": "integer",
            "minimum": 1,
            "maximum": 9999,
            "description": "The number of samples (data points) that this data set consists of."
        },
        "frequency": {
            "type": "number",
            "minimum": 0,
            "description": "The frequency (in Hertz) in which the sample values will be sent."
        },
        "calculationMethod": {
            "type": "string",
            "oneOf": [
                {
                    "const": CalculationMethod.ADDITIVE,
                    "title": "Additive"
                },
                {
                    "const": CalculationMethod.MULTIPLICATIVE,
                    "title": "Multiplicative"
                }
            ],
            "description": "Dictates the composition operation that will be used to combine the trend, season and residual values."
        }
    },
    "required": [
        "name",
        "numSamples",
        "frequency",
        "calculationMethod"
    ]
}
export default numericSchema;