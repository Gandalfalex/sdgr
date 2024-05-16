---
title: "file handling"
date: 2023-12-08T19:22:33+01:00
tags: []
featured_image: ""
description: ""
---



## File upload:
This document outlines the process for uploading files in supported formats, including JSON, NumPy, and CSV. The process includes validation, data handling, and conversion into a structured format.

### Supported File Types and Validation
- File Types: The system supports JSON, NumPy, and CSV file formats.
- Multiple Files: Users can upload multiple files simultaneously.
- Format Validation: The process breaks if any file is in the wrong format.
- File Size Limitation: Files larger than 10MB are rejected.

### General Process
- Check File Requirements: Verify if the file meets size and format requirements.
- Filetype Handling: Depending on the filetype (JSON, NumPy, or CSV), handle the file accordingly.
- Data Saving: Once processed, the data is saved.
- Return ID: The system returns the ID of the generated TrainingData object.

### Uploading JSON
#### List in JSON:
- One-Dimensional: Assume it's strict time series data without timestamps.
- Multi-Dimensional: Identify a list with regular intervals as timestamps. If none, treat each list separately and build a default timestamp list.
- Output: Create a dictionary {name: {value: timeSeries, time: timestamp}}.

#### Dictionary in JSON:
- Timestamp Mapping: Find a timestamp for each taxonomy and map other keys to it.
- No Timestamp: Treat each key as a separate list and generate a default timestamp list.
- Output: Create a dictionary {name: {value: timeSeries, time: timestamp}}.

{{<mermaid align="left">}}
flowchart TD
    A[Start: Check JSON Data] -->|List| B[Is it 1-Dimensional?]
    B -- Yes --> C[Assume Time Series Data Without Timestamps]
    C --> U[Create Dictionary]
    B -- No --> E[Multi-Dimensional Data]
    F --> P[Create Dictionary]
    E --> H[No Regular Intervals]
    E --> F[Identify List with Regular Intervals<br />and use as  Timestamp]
    H --> I[Treat each list separately,<br />Generate Default Timestamp]
    I --> U[Create Dictionary <br /> Headers as key, <br />Time Series and default Timestamps as value]
    A -->|Dictionary| K[Find Timestamp for Each Taxonomy]
    K --> L[Map Other Keys to Timestamp]
    L --> P
    K --> N[No Timestamp Found]
    N --> O[Treat Each Key as Separate List,<br />Generate Default Timestamp]
    O --> P[Create Dictionary <br /> Headers as key, <br />Time Series and Stamp as value]
{{< /mermaid >}}

### Uploading NumPy
- Process: Similar to handling JSON but without the dictionary part.
- One-Dimensional Array: Use Array as time series data and build default array.
- Multi-Dimensional Arrays: Check for regular intervals for timestamps; otherwise, use a default timestamp list.
- Output: Create a dictionary {name: {value: timeSeries, time: timestamp}}.

### Uploading CSV
- Header Identification: Use taxonomy to identify headers corresponding to timestamps.
- Timestamp Formats: Handle various timestamp formats using Pandas to_datetime() method for conversion to Unix time.
- No Timestamp Header: Build a default timestamp list.
- Column Validation: Ignore columns that don't contain int or float values.
- Output: Create a dictionary as in the previous steps.

