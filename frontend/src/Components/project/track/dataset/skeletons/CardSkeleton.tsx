import React, {ReactNode, useState} from 'react';
import {Box, Button, Card, CardContent, CardHeader, MobileStepper} from '@mui/material';
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import {DataType} from "../../../../../typedefs/spring_types";
import {OptionsMenu} from "../../../../shared_components/OptionsMenu";
import {useTranslation} from "react-i18next";

interface CardSkeletonProps {
    title: string;
    dataType: DataType;
    onEdit: () => void;
    onDelete: () => void;
    children: ReactNode[];
    totalSteps: number;
}

export const CardSkeleton: React.FC<CardSkeletonProps> = ({title, onEdit, onDelete, children, totalSteps, dataType}) => {
    const [activeStep, setActiveStep] = useState(0);
    const { t } = useTranslation(['components']);

    return (
        <Card sx={{height: "380px", width: "300px", maxWidth: "80vw", ml: 2}}>
            <CardHeader
                title={title}
                subheader={(activeStep === 0)
                    ? t('data_set_headline_info', {ns: ['components']})
                    : (activeStep === 1) ? t('data_set_headline_graph', {ns: ['components']})
                        : t('data_set_headline_individual', {ns: ['components']})}
                action={
                    <OptionsMenu
                        value={"config"}
                        setShowEditDialog={onEdit}
                        setShowDeleteDialog={onDelete}
                    />
                }
            />
            <CardContent sx={{'&:last-child': {pb: 0, pt: 0}}}>
                <Box sx={{height: "240px", overflow: "hidden"}}>
                    {children[activeStep]}
                </Box>
                {totalSteps !== 1
                    ? <MobileStepper
                        variant="dots"
                        steps={totalSteps}
                        position="static"
                        activeStep={activeStep}
                        nextButton={
                            <Button size="small"
                                    onClick={() => setActiveStep((prevActiveStep) => Math.min(prevActiveStep + 1, totalSteps - 1))}
                                    disabled={activeStep === totalSteps - 1}>
                                <KeyboardArrowRight/>
                            </Button>
                        }
                        backButton={
                            <Button size="small"
                                    onClick={() => setActiveStep((prevActiveStep) => Math.max(prevActiveStep - 1, 0))}
                                    disabled={activeStep === 0}>
                                <KeyboardArrowLeft/>
                            </Button>
                        }
                    />
                    : null}
            </CardContent>
        </Card>
    );
};

