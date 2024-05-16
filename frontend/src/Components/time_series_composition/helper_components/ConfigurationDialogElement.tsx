import React, {useEffect, useState} from "react";
import {getTsdConfigurationData} from "../../../api/DjangoAPI";
import TSAConfigGraph from "../../graphs/TSAConfigGraph";
import {Box, Button, MobileStepper, Paper, useTheme} from "@mui/material";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import {TSDConfig, TSDConfigData} from "../../../typedefs/django_types";
import TrainDataPreviewGraph from "../../graphs/TrainDataPreviewGraph";
import {OneDisplayOnlyElementsGraph} from "../../graphs/OneDisplayOnlyElements";


interface TSDConfigElementProps {
    element: TSDConfig
    send: (trainDataId: number, activeStep: number) => void;
}

type ConfigurationCardProps = TSDConfigElementProps & {
    previewData?: Array<TSDConfigData>;
    setPreviewData?: React.Dispatch<React.SetStateAction<Array<TSDConfigData>>>;
    allOffsets?: { [step: number]: { [key: string]: number } };
    setAllOffsets?: React.Dispatch<React.SetStateAction<{ [step: number]: { [key: string]: number } }>>;
};

export const ConfigurationCard = (props: ConfigurationCardProps) => {
    const {
        element,
        send,
        previewData: externalPreviewData,
        setPreviewData: externalSetPreviewData,
        allOffsets: externalAllOffsets,
        setAllOffsets: externalSetAllOffsets
    } = props;

    const [internalPreviewData, setInternalPreviewData] = useState<Array<TSDConfigData>>([]);
    const [internalAllOffsets, setInternalAllOffsets] = useState<{ [step: number]: { [key: string]: number } }>({});

    const effectivePreviewData = externalPreviewData ?? internalPreviewData;
    const effectiveSetPreviewData = externalSetPreviewData ?? setInternalPreviewData;

    const effectiveAllOffsets = externalAllOffsets ?? internalAllOffsets;
    const effectiveSetAllOffsets = externalSetAllOffsets ?? setInternalAllOffsets;


    const theme = useTheme();
    const [steps, setSteps] = useState<Array<string>>([]);
    const [activeStep, setActiveStep] = React.useState(0);


    useEffect(() => {
        // element.tsd_model, element.id
        if (effectivePreviewData.length === 0) {
            getTsdConfigurationData(element.tsd_model, element.id).then(res => {
                effectiveSetPreviewData(res)
                setSteps(res.map((r: { name: string; }) => r.name))
            })
        } else {
            setSteps(effectivePreviewData.map((r: { name: string; }) => r.name))
        }
    }, [effectiveAllOffsets, effectivePreviewData, effectiveSetPreviewData, element.id, element.tsd_model]);
    // @ts-ignore
    return (<div>
            {steps.length !== 0 ?
                (<div>
                    <Box sx={{p: 2}}>
                        {steps[activeStep]}
                    </Box>
                    <Paper
                        square
                        elevation={1}
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            pl: 2,
                            width: "90vh", maxWidth: 800,
                            bgcolor: 'background.default',
                        }}
                    >
                        <div style={{flexGrow: 1}}>

                            {effectivePreviewData[activeStep].type === "one_display"
                                ?
                                //@ts-ignore
                                <OneDisplayOnlyElementsGraph
                                    data={{name: "abs", values: internalPreviewData[0].values[0].data}} key={1}/>
                                :
                                <TSAConfigGraph
                                    configuration={effectivePreviewData[activeStep]}
                                    element={element}
                                    offsets={effectiveAllOffsets[activeStep] || {}}
                                    setActiveOffsets={(newOffsets) => {
                                        effectiveSetAllOffsets((prevOffsets) => ({
                                            ...prevOffsets,
                                            [activeStep]: newOffsets,
                                        }));
                                    }}
                                    send={trainDataId => send(trainDataId, activeStep)}
                                />

                            }
                        </div>
                    </Paper>
                    <MobileStepper
                        variant="text"
                        steps={effectivePreviewData.length}
                        position="static"
                        activeStep={activeStep}
                        nextButton={
                            <Button
                                size="small"
                                onClick={() => setActiveStep((prevActiveStep) => prevActiveStep + 1)}
                                disabled={activeStep === effectivePreviewData.length - 1}
                            >
                                Next
                                {theme.direction === 'rtl' ? (<KeyboardArrowLeft/>) : (<KeyboardArrowRight/>)}
                            </Button>
                        }
                        backButton={
                            <Button size="small" onClick={() => setActiveStep((prevActiveStep) => prevActiveStep - 1)}
                                    disabled={activeStep === 0}>
                                {theme.direction === 'rtl' ? (<KeyboardArrowRight/>) : (<KeyboardArrowLeft/>)}
                                Back
                            </Button>
                        }
                    />
                </div>)
                : null
            }
        </div>
    );
}

