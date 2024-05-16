import {Box, Button, Dialog} from '@mui/material';
import {SelectFormControl} from "../../../../../shared_components/SelectFormControl";
import {ConfigurationCard} from "../../../../../time_series_composition/helper_components/ConfigurationDialogElement";
import {useEffect, useState} from "react";
import {SelectChangeEvent} from "@mui/material/Select";
import {TrainDataDTO} from "../../../../../../typedefs/spring_types";
import {getTsdConfigurationDataForSingleDataSet} from "../../../../../../api/DjangoAPI";
import {findAllTrainDataOfConfiguration} from "../../../../../../api/SpringAPI";
import {TSDConfigData} from "../../../../../../typedefs/django_types";

interface TrainSelectProps {
    selectedModelId: number;
    selectedConfigurationId: number;
    setSelectedTrainData: (data: Array<TrainDataDTO>) => void;
    selectedTrainData: Array<TrainDataDTO>;
    oldTrainingData?: Array<number>;
    setAllOffsets: (data: ((prevState: { [p: number]: { [p: string]: number } }) => {
        [p: number]: { [p: string]: number }
    }) | { [p: number]: { [p: string]: number } }) => void;
    allOffsets: { [step: number]: { [key: string]: number } };
}

export const SelectTrainDataStep = (props: TrainSelectProps) => {

    const {
        selectedModelId,
        selectedConfigurationId,
        setSelectedTrainData,
        selectedTrainData,
        setAllOffsets,
        allOffsets,
        oldTrainingData
    } = props;
    const [configData, setConfigData] = useState<Array<TSDConfigData>>([]);
    const [openConfiguration, setOpenConfiguration] = useState<boolean>(false);
    const [trainData, setTrainData] = useState<Array<TrainDataDTO>>([]);
    const handleTrainDataChange = (event: SelectChangeEvent<number | number[]>) => {
        const selectedIds = event.target.value as number[];
        setSelectedTrainData(trainData.filter(s => selectedIds.includes(s.id)));
    };

    const handleButtonClick = async () => {
        let newConfigData = [...configData];

        if (selectedTrainData.length !== 0) {
            for (let data of selectedTrainData) {
                const current = newConfigData.find(s => s.id === data.id);
                if (!current) {
                    const res = await getTsdConfigurationDataForSingleDataSet(selectedModelId, selectedConfigurationId, data.id);
                    newConfigData.push(res);
                }
            }
            newConfigData = newConfigData.filter(data => selectedTrainData.some(selected => selected.id === data.id));
        }
        setConfigData(newConfigData);
        setOpenConfiguration(true);
    };

    useEffect(() => {
        findAllTrainDataOfConfiguration(selectedModelId, selectedConfigurationId)
            .then(res => {
                setTrainData(res)
                if (oldTrainingData && oldTrainingData.length !== 0) {
                    let tempData = res as Array<TrainDataDTO>
                    let oldTrainData = tempData.filter(data => oldTrainingData.includes(data.id))
                    setSelectedTrainData(oldTrainData)
                }
            })
    }, [oldTrainingData]);
    return (
        <Box>
            <SelectFormControl
                label="Select training data"
                value={selectedTrainData.map(data => data.id)}
                handleChange={handleTrainDataChange}
                items={trainData}
                id="select-train-data"
                multiple
            />
            {
                configData && (
                    <Dialog open={openConfiguration} onClose={() => setOpenConfiguration(false)} maxWidth={"xl"}
                            fullScreen={false}>
                        <Box width={{width: "900"}}>
                            <ConfigurationCard
                                element={{
                                    id: selectedConfigurationId,
                                    name: "0",
                                    description: "string",
                                    processing: null,
                                    imputation_algorithm: null,
                                    min_length: 0,
                                    created_at: "string",
                                    tsd_model: selectedModelId,
                                    train_data: []
                                }}
                                previewData={configData}
                                allOffsets={allOffsets}
                                setAllOffsets={(offset) => {
                                    setAllOffsets(offset)
                                }}
                                send={() => console.log("sending data")}
                            />
                        </Box>
                    </Dialog>
                )
            }
            <Button onClick={handleButtonClick} disabled={selectedTrainData.length === 0}> show all data</Button>
        </Box>
    );
}
