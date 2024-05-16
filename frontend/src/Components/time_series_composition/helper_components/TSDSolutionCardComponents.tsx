import React, {useState} from 'react';
import {CardContent, Collapse} from "@mui/material";
import TrainDataPreviewGraph from "../../graphs/TrainDataPreviewGraph";
import {TrainDataPreviewDT, TSDConfig} from "../../../typedefs/django_types";
import {ConfigurationCard} from "./ConfigurationDialogElement";
import {postConfigForTsd} from "../../../api/DjangoAPI";
import {SnackbarSeverity} from "../../../typedefs/error_types";
import {useSnackbar} from "../../shared_components/snackbar/SnackbarContext";
import {OccurrencesCardComponent} from "../../shared_components/cards/OccurencesCardComponent";
import {findAllOccurancesOfTSDConfiguration} from "../../../api/SpringAPI";
import {InformationPaperComponent} from "../../shared_components/paper/InformationPaperComponent";


interface SolutionCardsProps {
    config: TSDConfig;
    expanded: boolean;
    trainData: Array<TrainDataPreviewDT> | null;
}


export const TSDSolutionCards = (props: SolutionCardsProps) => {
    const [allOffsets, setAllOffsets] = useState<{ [step: number]: { [key: string]: number } }>({});
    const {showMessage} = useSnackbar();


    const sendDataToServer = (trainDataId: number, activeStep: number) => {
        postConfigForTsd(props.config.tsd_model, props.config.id, trainDataId, allOffsets[activeStep])
            .then(res => showMessage("saved configuration", SnackbarSeverity.SUCCESS))
            .catch(err => showMessage("something went wrong, please try again", SnackbarSeverity.ERROR))
    };


    return (
        <CardContent>
            <div style={{display: 'flex', overflowX: 'auto', gap: '16px'}}>
                <InformationPaperComponent header={props.config?.description}>
                    <OccurrencesCardComponent id={props.config.id}
                                              fetchOccurrences={findAllOccurancesOfTSDConfiguration}/>
                </InformationPaperComponent>
                <ConfigurationCard
                    element={props.config}
                    allOffsets={allOffsets}
                    setAllOffsets={setAllOffsets}
                    send={(trainDataId, activeStep) => sendDataToServer(trainDataId, activeStep)}
                />
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
