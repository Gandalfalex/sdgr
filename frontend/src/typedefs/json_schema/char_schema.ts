import {JsonSchema7} from "@jsonforms/core";

const charSchema: JsonSchema7 = {
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
        "alphabet": {
            "type": "string",
            "description": "The alphabet."
        }
    },
    "required": [
        "name",
        "numSamples",
        "frequency",
        "alphabet",
    ]
}

export default charSchema;