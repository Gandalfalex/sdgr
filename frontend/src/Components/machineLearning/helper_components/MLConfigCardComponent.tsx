import React, {useEffect} from 'react';
import {CardContent, Collapse, Typography} from "@mui/material";
import {StartTrainElement} from '../StartTrainElement';
import TrainingsInformationElement from "../training_information/TrainingInformationElement";
import TrainDataPreviewGraph from "../../graphs/TrainDataPreviewGraph";
import {MlConfig, TrainDataPreviewDT} from "../../../typedefs/django_types";
import {OccurrencesCardComponent} from "../../shared_components/cards/OccurencesCardComponent";
import {findAllOccurancesOfMLConfiguration} from "../../../api/SpringAPI";
import {InformationPaperComponent} from "../../shared_components/paper/InformationPaperComponent";
import {useTranslation} from "react-i18next";
import {getMlConfigByModelIdAndConfigId} from "../../../api/DjangoAPI";


interface ConfigCardComponents {
    config: MlConfig;
    expanded: boolean;
    trainData: Array<TrainDataPreviewDT> | null;
    onUpdate: () => void;
}


export const MLConfigCardComponents = (props: ConfigCardComponents) => {
    const {t} = useTranslation(['headers', 'dialogs', 'components']);
    useEffect(() => {
        getMlConfigByModelIdAndConfigId(props.config.ml_model, props.config.id).then(res => {})
    }, []);
    return (
        <CardContent>
            <div style={{display: 'flex', overflowX: 'auto', gap: '16px'}}>
                <InformationPaperComponent header={props.config?.description}>
                    <Typography variant="body2" color="textSecondary" component="p">
                        {t('elementCount', {count: props.config?.train_data.length, ns: ['components']})}
                    </Typography>
                    <OccurrencesCardComponent
                        id={props.config.id}
                        fetchOccurrences={findAllOccurancesOfMLConfiguration}/>
                </InformationPaperComponent>
                {
                    props.config && props.config?.solution_id !== 0 ?
                        <InformationPaperComponent
                            header={t('ml_training_configuration_info', {ns: ['dialogs']})}>
                            <TrainingsInformationElement config={props.config}/>
                        </InformationPaperComponent>
                        : null
                }
                <InformationPaperComponent key={"start_train"}>
                    <StartTrainElement
                        id={props.config.id}
                        modelId={props.config.ml_model}
                        solution={props.config}
                        onUpdate={props.onUpdate}/>
                </InformationPaperComponent>
            </div>
            <Collapse in={props.expanded} timeout="auto" unmountOnExit>
                <div style={{display: 'flex', overflowX: 'auto'}}>
                    {props.trainData && props.trainData.length > 0
                        ? props.trainData.map((dataSet, index) =>
                            <TrainDataPreviewGraph data={dataSet} key={index}/>)
                        : null
                    }
                </div>
            </Collapse>
        </CardContent>
    );
};
