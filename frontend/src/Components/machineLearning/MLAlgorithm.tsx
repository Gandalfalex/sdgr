import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import {MlConfig, Model} from "../../typedefs/django_types";
import {getAllSolutionsByModelId, getMlConfigByModelIdAndConfigId, getMlModelById} from "../../api/DjangoAPI";
import {Grid} from "@mui/material";
import {MlConfigElement} from "./MlConfigElement";
import GenericAccordion from "../shared_components/GenericAccordion";
import {MlConfigDialog} from "../dialogs/MlConfigDialog";
import {PaperContainerComponent} from "../shared_components/paper/PaperComponent";
import {ElementCardComponent} from "../shared_components/cards/ElementCardComponent";
import {NewElementButton} from "../buttons/NewElementButton";

export const useMLData = (mlId: string | undefined) => {
    const [model, setMlModel] = useState<Model>();
    const [configs, setAllSolutions] = useState<Array<MlConfig>>([]);

    useEffect(() => {
        if (mlId) {
            getMlModelById(Number(mlId)).then(setMlModel);
            getAllSolutionsByModelId(Number(mlId)).then(setAllSolutions);
        }
    }, [mlId]);

    const refreshSolutions = () => {
        if (mlId) {
            getAllSolutionsByModelId(Number(mlId))
                .then(setAllSolutions);
        }
    };

    const refreshSingleSolution = (solutionId: number) => {
        getMlConfigByModelIdAndConfigId(Number(mlId), solutionId).then(res =>
            setAllSolutions(prevConfigs => prevConfigs.map(config => config.id === solutionId ? res : config))
        )
    }

    return {model, configs, refreshSolutions, refreshSingleSolution};
};


export const MLAlgorithm = () => {
    const {mlId} = useParams();
    const {model, configs, refreshSolutions, refreshSingleSolution} = useMLData(mlId);
    const [showNewMLSolutionDialog, setShowNewMLSolutionDialog] = useState(false);
    const [expandID, setExpandId] = useState<number | null>(null)
    const toggleNewMlSolutionDialog = (open: boolean) => {
        setShowNewMLSolutionDialog(open);
        if (!open) {
            refreshSolutions();
        }
    };

    if (!mlId) return <div/>;

    return (
        <PaperContainerComponent>
            <ElementCardComponent header={model?.name}>
                {configs && configs.length > 0
                    ? configs.map((config) => (
                        <Grid key={config.id} item xs={1}>
                            <GenericAccordion
                                expanded={config.id === expandID}
                                onChange={() => setExpandId(expandID === config.id ? null : config.id)}
                                details={
                                <MlConfigElement config={config} onRefresh={() => refreshSingleSolution}/>
                            }
                                header={config.name}
                            />
                        </Grid>
                    ))
                    : null}
                <NewElementButton message={"Create new ML Configuration"} handleClick={toggleNewMlSolutionDialog}/>
                <MlConfigDialog
                    id="new-track"
                    isEdit={false}
                    keepMounted
                    open={showNewMLSolutionDialog}
                    onClose={() => toggleNewMlSolutionDialog(false)}
                    value={{
                        id: 0,
                        name: "",
                        description: "",
                        created_at: "",
                        ml_model: parseInt(mlId),
                        train_data: [],
                        imputation_algorithm: null,
                        min_length: 0,
                        solution_id: 0,
                        is_running: "",
                        processing: null
                    }}
                    onUpdateRefresh={refreshSolutions}
                />
            </ElementCardComponent>
        </PaperContainerComponent>
    );
};

