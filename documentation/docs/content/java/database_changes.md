---
title: "Database Changes"
date: 2023-12-08T19:22:33+01:00
tags: []
featured_image: ""
description: ""
---

# Database Changes
## Schema Structure
This document provides an overview of the database schema used in Spring, detailing its structure and the relationships between its components. The database is designed primarily in Boyce-Codd Normal Form (BCNF), ensuring normalization for efficient data management.

### Projects
- Definition: The core entity in the database schema.
- Functionality: Represents a simple component in an application, analogous to a physical component with multiple sensors.

### Tracks
- Contained within: Projects
- Definition: A track is a collection of elements, akin to a sensor in a physical component.
- Characteristics:
  - Runs in parallel with other tracks.
  - Independent, not involved with other tracks.

### DataSets
- Contained within: Tracks
- Definition: The basic unit within a track.
- Functionality: Represents stages of a sensor, which collectively build a track.
- Types of Data: Each element consists of a series of datasets, each dataset containing a list of values. These values are crucial for displaying different stages of the data received.

## Advanced Features
### Inheritance and Casting
- Tools Used: Hibernate and JPQL (Java Persistence Query Language).
- Functionality: Facilitates easy access to new fields through inheritance and casting.

Custom DataSetTypes
- Variants: Includes types like Chars, Integers, Machine Learning, Time Series Decomposition Sets, and Sleep Sets.
- Implementation: Each type requires a custom mapper.

Data Serialization and Casting
- Tool Used: Jackson
- Purpose: Handles specific field casting, required by Hibernate for automatic casting into the appropriate classes.

### Restructure DataSets
The restructuring of datasets in Spring represents a significant shift from a fixed structure to a more dynamic and polymorphic approach. Here is an overview of the changes:

```java
@Entity
@Inheritance(strategy = InheritanceType.SINGLE_TABLE)
@Accessors(chain = true)
@Data
@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "type")
@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSet.class, name = "char"),
        @JsonSubTypes.Type(value = FloatDataSet.class, name = "float"),
        @JsonSubTypes.Type(value = IntegerDataSet.class, name = "integer"),
        @JsonSubTypes.Type(value = MlDataSet.class, name = "ml"),
        @JsonSubTypes.Type(value = TSADataSet.class, name = "tsa"),
        @JsonSubTypes.Type(value = SleepDataSet.class, name = "sleep")
})
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public abstract class PlainData implements DataTypeOption {

    @Id
    @Column(name = "id")
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    @Column(name = "position")
    private int position;
    @Column(name = "numSamples")
    private int numSamples;
    @Column(name = "frequency")
    private float frequency;
    @Column(name = "name")
    private String name;
    @Column(name = "dataType")
    private DataTypes dataType;

    @ElementCollection(fetch = FetchType.EAGER)
    @CollectionTable(name = "data_set_custom_values",
            joinColumns = {@JoinColumn(name = "data_set_id", referencedColumnName = "id")})
    @MapKeyColumn(name = "sample_number")
    @Column(name = "custom_value")
    private Map<Integer, Double> customValues;
}
```

The `PlainDataClass` class serves as the abstract base class for different types of datasets. It includes attributes like id, position, numSamples, frequency, name, and dataType. The customValues attribute is a map designed to hold custom values specific to each dataset. The class uses annotations for entity definition, JSON polymorphism, and data visibility.


```java
@JsonTypeInfo(
        use = JsonTypeInfo.Id.NAME,
        include = JsonTypeInfo.As.PROPERTY,
        property = "type")
@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSetDTO.class, name = "char"),
        @JsonSubTypes.Type(value = IntegerDataSetDTO.class, name = "integer"),
        @JsonSubTypes.Type(value = MlDataSetDTO.class, name = "ml"),
        @JsonSubTypes.Type(value = TSADataSetDTO.class, name = "tsa"),
        @JsonSubTypes.Type(value = FloatDataSetDTO.class, name = "float"),
        @JsonSubTypes.Type(value = SleepDataSetDTO.class, name = "sleep")
})
@Data
@Accessors(chain = true)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class PlainDataDTO {

    @Schema(name = "id", nullable = true, minimum = "1")
    private Long id;

    @Schema(name = "name", nullable = false, description = "name to identify the dataSet")
    @JsonProperty("name")
    private String name;

    @Schema(name = "numSamples", nullable = true, minimum = "1", description = "sample set")
    @JsonProperty("numSamples")
    private int numSamples;

    @Schema(name = "position", nullable = true, description = "position inside the track")
    @JsonProperty("position")
    private Integer position;

    @Schema(name = "frequency", nullable = false, description = "repetitions per second")
    @JsonProperty("frequency")
    private float frequency;

    @Schema(name = "dataType", nullable = false, description = "DataType saved in backend")
    @JsonProperty("dataType")
    private DataTypes dataType;

    @Schema(name = "customValues", description = "custom values for calculation")
    @JsonProperty("customValues")
    private JsonNode customValues;
}
```
The `PlainDataDTO` class is a Data Transfer Object representing the `PlainData` class for data transportation. It contains similar fields to `PlainData` with additional API documentation annotations. 
The customValues field uses JsonNode for a more flexible representation of custom values.

### Key Changes and Implementation
- Global Requirements: Datasets now focus on essential attributes like name, frequency, and sample values, making them more streamlined and adaptable.
- Polymorphism: The use of JSON polymorphism allows automatic mapping of JSON data to the specific dataset instance.
- Custom Mappers: The DataMapper class plays a crucial role in the transformation between the entity objects (`PlainData`) and their Data Transfer Object (DTO) counterparts (`PlainDataDTO`). This class utilizes several specific mappers and a custom value converter to handle different dataset types.
The DataMapper class is a vital component in the Spring database schema's restructured dataset approach. It ensures the seamless transformation between entity objects and DTOs, respecting the specific attributes and behaviors of each dataset type. This setup provides flexibility and scalability, allowing for easy addition or modification of dataset types in the system.
- Custom DTOs: Each dataset implementation requires a custom DTO that contains all required fields. They extend from the - `PlainDataDTO` to include all necessary fields.
These changes enhance the flexibility and scalability of the dataset structure in Spring, leveraging polymorphism and a unified base class to cater to a diverse range of data types.


### Tracks
- Concept: Tracks within the Spring database now have a direct association with specific DataTypes.
- User Control: When creating a track, users can now specify the DataTypes they wish to include. This enhancement adds a layer of customization and control, ensuring that each track aligns precisely with the intended data structure.



### Project
- User Linkage: Projects in the database are now linked to individual user entities. This change ensures that data is user-specific and secure.
- SQL Query Adaptations: SQL queries involving project data now require the inclusion of a user object. This approach enhances data security and personalization.
- JPA Interface and AOP: The Java Persistence API (JPA) interface leverages Java's default methods in combination with Aspect-Oriented Programming (AOP). This innovative approach uses thread-local storage for handling user data, enhancing both security and efficiency, while leaving the base code base nearly untouched.
- Data Access Strategy: The principle of 'convention over configuration' is emphasized, particularly in handling larger data structures. Users must now be more diligent in applying fetching and cascading strategies to manage data effectively.

### Schema
- Backend-Driven Schema Generation: The task of schema generation has been moved to the backend, reducing the load and complexity on the frontend, particularly in React-based applications.
- Customizable JsonSchema Templates: These templates are stored and can be dynamically extended to meet varying data requirements. This shift allows for greater flexibility in data management and reduces the need for frequent code changes.
- Benefits to Frontend: Frontend applications benefit from a more generic and adaptable approach. The backend's handling of schema changes allows for a more streamlined and efficient frontend development process.

### Entities provided by Django Project
- Read-Only Access: The Spring framework now has read-only access to certain database objects managed within a Django project.
- Shared Database Environment: Both Spring and Django project entities operate within the same database. This shared environment promotes consistency and streamlined data management across different platforms.