CREATE TABLE ml_model (
                          id SERIAL PRIMARY KEY,
                          name VARCHAR(255),
                          description TEXT,
                          i18n_key VARCHAR(255),
                          pyName VARCHAR(255),
                          created_at TIMESTAMP,
                          forcasting BOOLEAN
);

-- tsd_models table
CREATE TABLE tsd_models (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(255),
                            i18n_key VARCHAR(255),
                            description TEXT,
                            pyName VARCHAR(255),
                            display_type VARCHAR(255),
                            created_at TIMESTAMP
);

-- json_schemas table
CREATE TABLE json_schemas (
                              id INTEGER PRIMARY KEY,
                              schema TEXT,
                              schema_type INTEGER,
                              ui_schema TEXT
);

-- preprocessor_type table
CREATE TABLE preprocessor_type (
                                   id SERIAL PRIMARY KEY,
                                   name VARCHAR(255),
                                   description TEXT,
                                   schema_enum_value TEXT,
                                   schema TEXT
);

-- schema_validation_forms table
CREATE TABLE schema_validation_forms (
                                         id SERIAL PRIMARY KEY,
                                         name VARCHAR(255),
                                         schema TEXT,
                                         ui_schema TEXT
);

-- data_type table
CREATE TABLE data_type (
                           id SERIAL PRIMARY KEY,
                           data_type_name VARCHAR(255),
                           description TEXT,
                           preview_showing BOOLEAN,
                           data_type INTEGER,
                           schema_id INTEGER,
                           FOREIGN KEY (schema_id) REFERENCES json_schemas (id)
);

-- imputation_algorithm table
CREATE TABLE imputation_algorithm (
                                      id SERIAL PRIMARY KEY,
                                      name VARCHAR(255),
                                      description TEXT
);



