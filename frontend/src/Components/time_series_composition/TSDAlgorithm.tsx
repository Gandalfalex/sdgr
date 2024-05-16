import {useParams} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {getTSDConfigByModelId, getTsdModel} from "../../api/DjangoAPI";
import {Grid} from "@mui/material";
import {TSDConfigDialog} from "../dialogs/TSDConfigDialog";
import {TSDConfigElement} from "./TSDConfigElement";
import GenericAccordion from "../shared_components/GenericAccordion";
import {Model, TSDConfig} from "../../typedefs/django_types";
import {PaperContainerComponent} from "../shared_components/paper/PaperComponent";
import {ElementCardComponent} from "../shared_components/cards/ElementCardComponent";
import {NewElementButton} from "../buttons/NewElementButton";
import {useTranslation} from "react-i18next";

const useTSDData = (tsdId: string | undefined) => {
    const [model, setModel] = useState<Model>();
    const [configs, setAllConfigs] = useState<Array<TSDConfig>>([]);

    useEffect(() => {
        if (tsdId) {
            getTsdModel(Number(tsdId)).then(setModel);
            getTSDConfigByModelId(Number(tsdId)).then(setAllConfigs);
        }
    }, [tsdId]);

    const refreshConfigs = () => {
        if (tsdId) {
            getTSDConfigByModelId(Number(tsdId)).then(setAllConfigs);
        }
    };

    return {model, configs, refreshConfigs};
};


export const TSDAlgorithm = () => {
    const {tsdId} = useParams();
    const {model, configs, refreshConfigs} = useTSDData(tsdId);
    const [showNewTSDSolutionDialog, setShowNewTSDConfigDialog] = useState(false);
    const [expandID, setExpandId] = useState<number | null>(null);
    const {t} = useTranslation(['dialogs', 'headers']);
    const toggleNewTSDConfigDialog = (open: boolean) => {
        setShowNewTSDConfigDialog(open);
        if (!open) {
            refreshConfigs();
        }
    };

    if (!tsdId) return <div/>;

    return (
        <PaperContainerComponent>
            <ElementCardComponent
                header={model?.name}>
                {configs && configs.length > 0
                    ? configs.map((config) => (
                        <Grid key={config.id} item xs={1}>
                            <GenericAccordion
                                expanded={config.id === expandID}
                                onChange={() => setExpandId(expandID === config.id ? null : config.id)}
                                details={<TSDConfigElement config={config} onRefresh={refreshConfigs}/>}
                                header={config.name}
                            />
                        </Grid>
                    )) : null}
                <NewElementButton
                    message={t('new_tsa_config', {ns: ['dialogs']})}
                    handleClick={toggleNewTSDConfigDialog}/>
                <TSDConfigDialog
                    id="new-track"
                    isEdit={false} keepMounted
                    open={showNewTSDSolutionDialog}
                    onClose={() => toggleNewTSDConfigDialog(false)}
                    value={{
                        id: 0,
                        name: "",
                        created_at: "",
                        tsd_model: parseInt(tsdId),
                        imputation_algorithm: null,
                        min_length: 0,
                        train_data: [],
                        description: "",
                        processing: null,
                    }}
                    onUpdateRefresh={refreshConfigs}/>
            </ElementCardComponent>
        </PaperContainerComponent>
    );
}