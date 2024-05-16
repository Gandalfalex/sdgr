---
title: "Write a New Feature: Adding a Database Element"
author: "[Felix Fischer]"
description: "This guide walks through the steps of adding a new database element in a Java Spring application, covering backend and frontend changes."
tags: ["Java", "Spring", "Feature"]
---


# How to add new Datatypes:

## Start with the Entity

### Create the Package:
Build a package structure like this. Replace the name with your datatype
```
├── src
│   ├── adapter
│   │   ├── outbound
│   │   │   ├── entity
│   │   │   │   ├── extensions
│   │   │   │   │   ├── types
│   │   │   │   │   │   ├── DataType
│   │   │   │   │   │   ├── DataTypeDTO
│   │   │   │   │   │   ├── DataTypeMapper
```


#### 1. FileTypeDataSet
**Purpose**: Represents the data model for file datasets in the application. It's an entity class mapped to a database table.

**Annotations**:
- __@EqualsAndHashCode__, __@Data__, __@NoArgsConstructor__, __@Accessors__: Lombok annotations to reduce boilerplate for getter, setter, equals, hashCode, and no-arg constructor methods.
- __@Entity__: JPA annotation to mark it as a database entity.

**Fields and Methods**:
- __TrainData trainData__: A many-to-one relationship with another entity, TrainData.
- __calculatePreviewData__, __calculateData__, __getDataType__: Overridden methods to provide specific implementations for file datasets.
```java
@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Entity
@Accessors(chain = true)
public class FileDataSet extends PlainData {

    @ManyToOne(fetch = FetchType.EAGER)
    private TrainData trainData;

    @Override
    public JsonNode calculatePreviewData(int dataReductionThreshold, DataReducer dataReducer) {
        ...
        return node;
    }

    @Override
    public List<String> calculateData() {
        return trainData.getValues().stream().map(Object::toString).toList();
    }

    @Override
    public DataTypes getDataType() {
        return DataTypes.FILETYPE;
    }
}
```



#### 2. FileDataSetDTO (Data Transfer Object)

**Purpose**: Serves as a data transfer object. DTOs are used to transfer data between processes, in this case, to and from the API layer.

**Annotations**:
Similar to FileDataSet, Lombok annotations are used here for convenience.
- __@Schema__: Used for OpenAPI documentation.

**Fields**:
- __Long trainDataId__: Represents the ID of the TrainData entity.
- __DataTypes dataType__: A fixed value indicating the type of data (FILETYPE in this case).


```java
@EqualsAndHashCode(callSuper = true)
@Data
@NoArgsConstructor
@Accessors(chain = true)
public class FileDataSetDTO extends PlainDataDTO {

    @Schema(name = "trainDataId", description = "Id of the traindata element")
    @NotNull
    private Long trainDataId;

    @Schema(name = "dataType", nullable = false, description = "the dataType it represents")
    private final DataTypes dataType = DataTypes.FILETYPE;
}

```


#### 3. FileDataSetMapper (Service Layer)

**Purpose**: Responsible for converting between the entity object (FileDataSet) and the DTO (FileDataSetDTO). This is typically part of the service layer in an application.

**Annotations**:
- __@RequiredArgsConstructor__, __@Service__, __@Slf4j__: Lombok and Spring annotations for constructor injection, service declaration, and logging.

**Methods**:
- __toDTO__: Converts an entity object to its corresponding DTO.
- __toEO__: Converts a DTO back to an entity object, useful for create/update operations.
- __mergeDoToEO__: Helper method to update an existing entity object with new data from a DTO.
```java
@RequiredArgsConstructor
@Service
@Slf4j
public class FileDataSetMapper {

    private final TrainDataRepository trainDataRepository;

    @SneakyThrows
    public FileDataSetDTO toDTO(FileDataSet eo) {
        return new FileDataSetDTO()
                .setTrainDataId(eo.getTrainData().getId());
    }

    @SneakyThrows
    public FileDataSet toEO(FileDataSetDTO dto) {
        var temp = (FileDataSet) new FileDataSet().setId(dto.getId());
        return mergeDoToEO(temp, dto);
    }

    public FileDataSet mergeDoToEO(FileDataSet eo, FileDataSetDTO dto) {
        var traindata = trainDataRepository.findById(dto.getTrainDataId())
                .orElseThrow(() -> new EntityNotFoundException("TrainData does not exists"));
        return eo
                .setTrainData(traindata);
    }
}
```


#### Include in general Structure

Now the feature is build. It only has to be integrated into the generell Structure of the project.


```java
// Create a new DataType
@Getter
public enum DataTypes {

    CHAR("char"),
    ...
    FILETYPE("filetype");
}

// Add the DataType name to the JsonSubTypes.Type

@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSet.class, name = "char"),
        ...
        @JsonSubTypes.Type(value = FileDataSet.class, name = "filetype")
})
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public abstract class PlainData implements DataTypeOption {}
@JsonSubTypes({
        @JsonSubTypes.Type(value = CharDataSetDTO.class, name = "char"),
        ...
        @JsonSubTypes.Type(value = FileDataSetDTO.class, name = "filetype")
})
@Data
@Accessors(chain = true)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class PlainDataDTO {}

// Add the new Type into the PostConstructor of the DataMapper.
@Component
@RequiredArgsConstructor
@Slf4j
public class DataMapper {
    @PostConstruct
    public void init() {
        toDTOMap = new HashMap<>();
        toDTOMap.put(DataTypes.FLOAT, dataElement -> floatMapper.toDTO((FloatDataSet) dataElement));
        ...
        toDTOMap.put(DataTypes.FILETYPE, dataElement -> fileDataSetMapper.toDTO((FileDataSet) dataElement));

        toEOMap = new HashMap<>();
        ...
        toEOMap.put(DataTypes.FILETYPE, dataElement -> fileDataSetMapper.toEO((FileDataSetDTO) dataElement));
    }
}

// To create an ui entry, add it also as category into the Schema Enum. Here multiple types with the same appearance can be bundled.
public enum DataTypeSchema {
    NUMERIC(0L),
    ALPHABETIC(1L),
    ML(2L),
    TSA(3L),
    SLEEP(4L),
    FILETYPE(5L);
}
```

To make it visible, add a json schema to the database for this file.
```sql
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


INSERT INTO data_type (data_type_name, description, preview_showing, data_type, schema_id)
VALUES ('FILE', 'Chose one Element you want to send', 'True', '6', 6);
```


### Frontend changes
#### 1. Add the DataType
**Purpose**: Extend the application's data types to include FILETYPE.

**Implementation**:
- __DataSetType__: A TypeScript union type is defined to list all possible dataset types, including the newly added filetype.
- __DataType Enum__: This enum maps the data type strings to more formal enumeration values. FILETYPE = "FILETYPE" is added to this enum.
- __FileDataSet Interface__: Extends the base DataSet interface to represent the FILETYPE dataset specifically, including necessary properties like trainDataId.
- __Groups__: The GROUPS object categorizes different data types. FILETYPE is added to an appropriate group (GENERATED_DATA in this case) based on its characteristics or usage.

```javascript
type DataSetType = "float" | "integer" | "char" | "ml" | "tsa" | "sleep" | "filetype";

export enum DataType {
    FLOAT = "FLOAT",
    ...
    FILETYPE = "FILETYPE"
}

export interface FileDataSet extends DataSet {
    type: "filetype";
    trainDataId: number;
    dataType: DataType.FILETYPE;
}
// Add your Element to a group type, or write your own group.
export const GROUPS = {
    PRIMITIVE_DATA: [DataType.FLOAT, DataType.INTEGER, DataType.CHAR],
    GENERATED_DATA: [DataType.ML, DataType.TSA, DataType.FILETYPE],
    TIMING: [DataType.SLEEP],
};
```

This ensures that the Elements are known.

#### 2. you'll have to configure the DataSetHOC.


**Purpose**: Update the application's logic to handle the new FILETYPE dataset.

**Implementation**:
- __Generic Function for Casting__: getDataType<T> is a utility function that casts a dataset to its specific type based on the provided DataType.
- __DataTypeMap__: This mapping links each DataType to its corresponding React component wrapped in a higher-order component (withDataSet). 
You need to add the FILETYPE mapping to tis object.

- __DataSetProp__: Define a TypeScript type for the props of the FileDataSet component. This is useful for type safety and code clarity.


```javascript
// Create a generic function for casting.
export function getDataType<T>(type: DataType, element: T) {
    switch (type) {
        case DataType.FLOAT:
            return element as FloatDataSet
        ...
        case DataType.FILETYPE:
            return element as FileDataSet
        case DataType.NONE:
            return element
    }
}
// Add the element to the DataTypeMap
export const DataSetTypeMap = {
    [DataType.FLOAT]: withDataSet(FloatDataSetElement),
    ...
    [DataType.NONE]: withDataSet(SleepDataSetElement),
};

// and write an DataSetProp. This is optional
export type FileDataSetProps = DataSetProps<FileDataSet>;
```

#### 3. create a new Component to render the element.

**Purpose**: Provide a UI representation and interaction for the FILETYPE dataset.

**Implementation**:
- __Component Structure__: The FileDataSetElement component is structured to handle UI elements like preview data, data overview, and custom value editing.
- __State and Effects__: Use React's useState and useEffect to manage and update the preview data.
- __Data Handling__: Fetch and display data specific to FILETYPE, such as preview data, overview, and single values.

```javascript
export const FileDataSetElement = (props: FileDataSetProps) => {
    const {projectId, trackId, dataSet} = props;
    const {handleUpdateCustomValues, handleDelete, handleEdit} = useDataSetElement(props);

    const [previewData, setPreviewData] = useState<PreviewData>();

    let data = createData<FileDataSet>(dataSet)

    // update preview when dataset changes
    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [dataSet]) // eslint-disable-line react-hooks/exhaustive-deps

    useEffect(() => {
        getDataSetPreview(projectId, trackId, dataSet.id).then(res => setPreviewData(res));
    }, [])  // eslint-disable-line react-hooks/exhaustive-deps


    return (
        <CardSkeleton title={dataSet?.name}
                      dataType={dataSet.dataType}
                      onEdit={handleEdit}
                      onDelete={handleDelete}
                      totalSteps={3}>
            <OverviewTableContainer data={data}/>
            <PreviewDataContainer previewData={previewData}/>
            <SingleValues dataSet={dataSet} updateDataSet={handleUpdateCustomValues}/>
        </CardSkeleton>
    );
}
```