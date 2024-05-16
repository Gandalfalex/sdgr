---
title: "Machine learning"
date: 2023-12-08T19:22:33+01:00
tags: []
featured_image: ""
description: ""
---



## Training the Machine Learning Model Process

### Overview
The training process for the machine learning model is initiated upon receiving a new request via a WebSocket connection. This process involves retrieving data and configurations, processing the data, training the model, and saving the results along with the model itself.

### Steps in the Training Process

#### 1. Data Preparation
- Upon a WebSocket request, the training data and configurations are retrieved from the database.
- A `ProcessingBuilder` object is created using the Builder pattern, allowing for the configuration of necessary data processing steps.

#### 2. Setting Up Run Information
- Used MLModel is determined using strategy pattern, allowing for easy extension
- A `RunInformation` object is created to hold essential details required by the ML model and for later database storage.

#### 3. Model Initialization and Training Setup
- The `MLRunner` takes the `ProcessingBuilder` and `RunInformation` objects.
- It processes the data and takes care of eventual gaps.
- If large gaps exist, it trains a separate classifier model to identify these gaps
- The training process begins, with callbacks added for post-processing steps.

#### 4. Training the Model
- The model training is a long-running, iterative task.
- Status updates are sent to the user via WebSocket throughout the training process.

#### 5. Saving the Trained Model
- After training, the model is saved to a temporary file. (.keras) and converted to base64
- A visual representation (e.g., a .png image) of the model's solution is created and saved.

#### 6. Storing Results and Model in Database
- Important values such as runtime, iterations, and loss are recorded in the database.
- The model itself is also saved, typically converted to a base64 format for storage.

#### 7. Finalization
- Once the training and saving processes are complete, the WebSocket connection is terminated.

### Key Components

- **ProcessingBuilder**: Used for setting up data processing workflows.
- **RunInformation**: Holds necessary information for ML model training and data storage.
- **MLRunner**: Coordinates the training process, interfacing between data processing and the ML model.
- **ProcessingPool**: Manages the processing of data in preparation for training.
- **WebSocket Connection**: Facilitates real-time communication for status updates during the training process.


### Datastructure of ML models:

```
\model_training
    base_model.py
    ml_runner.py 
    ml_strategy.py
    run_information.py
    general_model.py (base class)
    \algorithm_implementation
        ...
```

### Conclusion
This process ensures a comprehensive approach to ML model training, encompassing data preparation, processing, model training, and the storage of results. The utilization of WebSocket for real-time updates enhances user engagement and transparency during the training phase.
