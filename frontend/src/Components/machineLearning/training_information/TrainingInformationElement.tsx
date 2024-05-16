import React, {useEffect, useState} from "react";
import {MlConfig, TrainingInformation} from "../../../typedefs/django_types";
import {getInformationAboutConfiguration} from "../../../api/DjangoAPI";
import moment from "moment";
import {ImageContainerView} from "./ImageContainerView";
import {useTranslation} from "react-i18next";

interface TrainingInformationProps {
    config: MlConfig
}


const TrainingsInformationElement = (props: TrainingInformationProps) => {
    const [data, setData] = useState<TrainingInformation>()
    const {config} = props;
    const { t } = useTranslation(['dialogs']);
    useEffect(() => {
        getInformationAboutConfiguration(config.ml_model, config.solution_id).then(res => setData(res));
    }, [config]);
    return (
        <div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                <span>{t('ml_training_stat_information_id', {ns: ['dialogs']})}</span>
                <span>{data?.ml_solution_id}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                <span>{t('ml_training_stat_information_added_to', {ns: ['dialogs']})}</span>
                <span>{moment(data?.added_to).format('DD.MM.YYYY, hh:mm')}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                <span>{t('ml_training_stat_information_time', {ns: ['dialogs']})}</span>
                <span>{data?.training_time}s</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                <span>{t('ml_training_stat_information_iterations', {ns: ['dialogs']})}</span>
                <span>{data?.iterations}</span>
            </div>
            <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '8px'}}>
                <span>{t('ml_training_stat_information_loss', {ns: ['dialogs']})}</span>
                <span>{data?.accuracy}</span>
            </div>

            {data?.image ? <ImageContainerView base64Image={data.image}/> : null}

        </div>);
}
export default TrainingsInformationElement;