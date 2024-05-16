import {InformationPaperComponent} from "../shared_components/paper/InformationPaperComponent";
import {CardContent} from "@mui/material";
import React, {useMemo, useState} from "react";
import {TrainDataInformation, TrainDataPreviewComplete, TrainingData} from "../../typedefs/django_types";
import {getSpecificTrainingData, getSpecificTrainingDataIformation} from "../../api/DjangoAPI";
import {GapIncludingGraphElement} from "../graphs/GapIncludingGraphElement";
import moment from "moment";
import {Stack} from "@mui/system";

interface TrainingDataSetProp {
    data: TrainingData;
}

export const DataViewComponents = (props: TrainingDataSetProp) => {
    const {data} = props;
    const [trainData, setTrainData] = useState<TrainDataPreviewComplete | null>(null)
    const [information, setInformation] = useState<TrainDataInformation | null>(null)

    const formatValue = (key: string, value: any) => {
        if (typeof value === 'boolean') {
            return value ? 'True' : 'False';
        }
        switch (key) {
            case 'added_to':
                return moment(value).format('DD.MM.YYYY, hh:mm');
            case 'training_time':
                return `${value}s`;
            default:
                return value;
        }
    };

    useMemo(() => {
        getSpecificTrainingData(data.id).then(res => {
            setTrainData(res)
        })
        getSpecificTrainingDataIformation(data.id).then(res => {
            setInformation(res)
        })
    }, []);

    return <CardContent>
        <Stack spacing={2}>
            {trainData ?
                <InformationPaperComponent>
                    <GapIncludingGraphElement
                        data={trainData.original}
                        flags={trainData.flags}/>
                </InformationPaperComponent>
                : null
            }
            {information ?
                <InformationPaperComponent>
                    <div>
                        {information ?
                            Object.entries(information!).map(([key, value]) => (
                                <div key={key}
                                     style={{
                                         display: 'flex',
                                         justifyContent: 'space-between',
                                         marginBottom: '8px'
                                     }}>
                                    <span>{key.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}</span>
                                    <span>{formatValue(key, value)}</span>
                                </div>
                            )) : null}
                    </div>
                </InformationPaperComponent>
                : null
            }
        </Stack>
    </CardContent>
}

