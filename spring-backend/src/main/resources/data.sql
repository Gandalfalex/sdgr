INSERT INTO ml_model (name, description,"i18n_key", "pyName", created_at, forcasting)
VALUES ('GAN',
        'This is a simple GAN model',
        'gan_model',
        'GAN.py',
        '1990-01-01 00:00:00.000 +0100',
        false);

INSERT INTO ml_model (name, description,"i18n_key",  "pyName", created_at, forcasting)
VALUES ('RNN',
        'This is a simple RNN model, implementation differs from GAn',
        'rnn_model',
        'RNN.py',
        '1990-01-01 00:00:00.000 +0100',
        false);

INSERT INTO ml_model (name, description,"i18n_key",  "pyName", created_at, forcasting)
VALUES ('CNN',
        'This is a simple CNN model',
        'cnn',
        'CNN.py',
        '1990-01-01 00:00:00.000 +0100',
        false);
INSERT INTO ml_model (name, description,"i18n_key",  "pyName", created_at, forcasting)
VALUES ('CGAN',
        'Conditional Generative Adversarial Networks introduces additional conditional variables to the generator and discriminator, providing control over the generated data',
        'cgan_model',
        'CGAN.py',
        '1990-01-01 00:00:00.000 +0100',
        false);

INSERT INTO ml_model (name, description,"i18n_key",  "pyName", created_at, forcasting)
VALUES ('LSTM',
        'This is a simple LSTM model',
        'lstm_model',
        'LSTM.py',
        '1990-01-01 00:00:00.000 +0100',
        false);

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('EMD',
        'emd_model',
        'Empirical Mode Decomposition',
        'EMD.py',
        'split',
        '1990-01-01 00:00:00.000 +0100');

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('SSA',
        'ssa_model',
        'Singular Spectrum Analysis',
        'SSA.py',
        'split',
        '1990-01-01 00:00:00.000 +0100');

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('Cubic Spline',
        'cubic_model',
        'Cubic something',
        'CUBIC_SPLINE.py',
        'one_display',
        '1990-01-01 00:00:00.000 +0100');

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('Amira',
        'amira',
        'Amira model',
        'AMIRA.py',
        'one_display',
        '1990-01-01 00:00:00.000 +0100');

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('SARIMAXModel',
        'sarmimax_model',
        'Amira model',
        'SARIMAXModel.py',
        'one_display',
        '1990-01-01 00:00:00.000 +0100');

INSERT INTO tsd_models (name, "i18n_key", description, "pyName", "display_type", created_at)
VALUES ('VAR',
        'var',
        'var model',
        'VAR.py',
        'one_display',
        '1990-01-01 00:00:00.000 +0100');



INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (1,
        '{"type": "object", "required": ["name", "numSamples", "frequency", "calculationMethod", "trend", "season", "residual"], "properties": {"name": {"type": "string", "description": "data_set_name"}, "trend": {}, "season": {}, "residual": {}, "frequency": {"type": "number", "minimum": 0, "description": "data_set_frequency"}, "numSamples": {"type": "integer", "maximum": 9999, "minimum": 1, "description": "data_set_samples"}, "calculationMethod": {"enum": ["additive", "multiplicative"], "type": "string", "description": "data_set_calculation"}}}',
        0,
        '{"ui:order": ["name", "numSamples", "frequency", "calculationMethod", "trend", "season", "residual", "trendOption", "seasonOption", "residualOption"], "calculationMethod": {"ui:widget": "radio", "ui:options": {"inline": true}, "ui:placeholder": "Choose an option"}, "ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');


INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (2,
        '{"type": "object",
        "required": ["name", "numSamples", "frequency", "alphabet"],
        "properties": {
           "name": {"type": "string","description": "data_set_name"},
           "alphabet": {"type": "array","items": {"type": "string","minLength": 1,"maxLength": 1},
           "description": "data_set_alphabet"},
           "frequency": {"type": "number","minimum": 0,"description": "data_set_frequency"},
           "numSamples": {"type": "integer","maximum": 9999,"minimum": 1,"description": "data_set_samples"}
        }}',
        1,
        '{"ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');



INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (3,
        '{"type": "object","required": ["name","numSamples","frequency","generation_option"],"properties": {"name": {"type": "string","description": "data_set_name"},"frequency": {"type": "number","minimum": 0,"description": "data_set_frequency"},"numSamples": {"type": "integer","maximum": 9999,"minimum": 1,"description": "data_set_samples"}}}',
        2,
        '{"generation_option": {"ui:widget": "radio", "ui:options": {"inline": true}, "ui:placeholder": "Choose an option"}, "ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');

INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (4,
        '{"type": "object", "required": ["name", "numSamples", "frequency","generation_option"], "properties": {"name": {"type": "string", "description": "data_set_name"}, "frequency": {"type": "number", "minimum": 0, "description": "data_set_frequency"}, "numSamples": {"type": "integer", "maximum": 9999, "minimum": 1, "description": "data_set_samples"}}}',
        3,
        '{"generation_option": {"ui:widget": "radio", "ui:options": {"inline": true}, "ui:placeholder": "Choose an option"}, "ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');

INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (5,
        '{"type": "object", "required": ["name", "sleepTime"], "properties": {"name": {"type": "string", "description": "data_set_name"}, "sleepTime": {"type": "integer", "maximum": 9999, "minimum": 1, "description": "data_set_sleep"}}}',
        4,
        '{"ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');

INSERT INTO json_schemas (id, schema, schema_type, ui_schema)
VALUES (6,
        '{"type": "object",
          "required": ["name", "numSamples", "frequency", "trainDataId"],
          "properties": {
            "name": {"type": "string","description": "data_set_name"},
            "trainDataId": {"type": "integer","minimum": 1,"description": "data_set_train_id"},
            "frequency": {"type": "number","minimum": 0,"description": "data_set_frequency"},
            "numSamples": {"type": "integer","maximum": 9999,"minimum": 1,"description": "data_set_samples"}
          }}',
        5,
        '{"ui:submitButtonOptions": {"props": {"disabled": false, "className": "btn btn-info"}, "norender": true, "submitText": "Submit"}}');



INSERT INTO preprocessor_type (name, description, schema_enum_value,  schema)
VALUES ('LinearTrendRemove',
        'Linear Trend Remove',
        'remove the linear trend of a given series',
        '{"properties": {"a": {"type": "integer","description": "preprocessing.linear_slope"},"b": {"type": "integer","description": "preprocessing.linear_intercept"},"t": {"type": "array","items": {"type": "number"},"description": "preprocessing.linear_time_array"}},"required": ["a","b","t"]}');

INSERT INTO preprocessor_type (name, description, schema_enum_value,  schema)
VALUES ('SimpleReduction',
        'devide any value by the largest absolute value)',
        'Simple Reduction',
        '{"properties": {"max_red": {"type": "integer","description": "preprocessing.reduction_max"}},"required": ["max_red"]}');

INSERT INTO schema_validation_forms (name, schema, ui_schema)
VALUES ('default_validation_schema',
        '{
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Data Processing Configuration",
        "description": "Schema for specifying data processing configuration with customizable options",
        "type": "object",
        "properties": {"min_length": {"type": "integer", "description": "validation_forms.min_length"}},
        "required": ["min_length"]}',
        '{"ui:submitButtonOptions": {"props": {"disabled": false,"className": "btn btn-info"},"norender": true,"submitText": "Submit"}}');

INSERT INTO schema_validation_forms (name, schema, ui_schema)
VALUES ('customization_option',
        '{"properties": {"configuration option": {"type": "string","enum": ["default option","customize"],"default": "default option","description": "validation_forms.config_option"}},"required": ["configuration option"],"if": {"properties": {"configuration option": {"const": "customize"}}}}',
        '{"configuration option": {"ui:widget": "radio","ui:options": {"inline": true},"ui:placeholder": "Choose an option"}}');

INSERT INTO schema_validation_forms(name, schema, ui_schema)
VALUES ('forecasting_option',
        '{"allOf": [{"if": {"properties": {"generation_option": {"const": "FORECAST"}}},"then": {"required": ["start_value","prediction_length"],"properties": {"start_value": {"type": "integer","maximum": 9999,"minimum": 1,"description": "validation_forms.forecasting"},"prediction_length": {"type": "integer","maximum": 999,"minimum": 1,"description": "validation_forms.prediction_length"}}}}]}',
        '{"generation_option": {"ui:widget": "radio","ui:options": {"inline": true},"ui:placeholder": "choose generation of data of forecasting"}}'
        );




INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('INTEGER', 'Integer values only', 'True', '4', 1);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('FLOAT', 'float values', 'True', '1', 1);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('CHAR', 'alphabet', 'True', '0', 2);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('ML', 'Machine Learning', 'True', '2', 3);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('TSA', 'Time Series Analysis', 'True', '3', 4);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('SLEEP', 'Sleep time of the element', 'False', '5', 5);

INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('FILE', 'Chose one Element you want to send', 'True', '6', 6);

INSERT INTO imputation_algorithm (name, description)
VALUES ('LOCF', 'Perform Last Observation Carried Forward imputation on an array, replacing NaN values with the last observed value');
INSERT INTO imputation_algorithm (name, description)
VALUES ('MEAN', 'Perform mean imputation on an array, replacing NaN values with the mean of the array');
INSERT INTO imputation_algorithm (name, description)
VALUES ('MEDIAN', 'Perform median imputation on an array, replacing NaN values with the median of the array');
INSERT INTO imputation_algorithm (name, description)
VALUES ('NOCF', 'Perform Next Observation Carried Backward (NOCB) imputation on an array, replacing NaN values with the next observed value');
INSERT INTO imputation_algorithm (name, description)
VALUES ('SPLINE INTERPOLATION', 'Perform spline interpolation on a 1D array with missing values');