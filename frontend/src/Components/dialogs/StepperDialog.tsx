import React, {FC, useState} from 'react';
import {
    Backdrop,
    Button,
    CircularProgress,
    Container,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Step,
    StepLabel,
    Stepper,
} from '@mui/material';
import {SaveData} from "../../typedefs/error_types";
import {DialogActionComponent} from "./DialogActionsComponent";
import {useTranslation} from "react-i18next";

interface StepperDialogProps {
    open: boolean;
    steps: string[];
    getStepContent: (step: number) => JSX.Element;
    activeStep: number;
    setActiveStep: (step: number) => void;
    handleCancel: () => void;
    send: () => void;
    isEdit: boolean;
    isSubmittable: () => SaveData;
}

export const StepperDialog: FC<StepperDialogProps> = ({
                                                          open,
                                                          steps,
                                                          getStepContent,
                                                          handleCancel,
                                                          send,
                                                          isEdit,
                                                          isSubmittable,
                                                          activeStep,
                                                          setActiveStep
                                                      }) => {
    const [openBackDrop, setOpenBackDrop] = useState(false);
    const [showInvalidInput, setShowInvalidInput] = useState(false);
    const [showWarningNotValidConfig, setShowWarningNotValidConfig] = useState(false);
    const {t} = useTranslation(['dialogs', 'headers']);
    const handleCloseBackDrop = () => {
        setOpenBackDrop(false);
    };

    const handleConfirmSubmit = () => {
        setShowWarningNotValidConfig(false);
        send();
    };

    return (
        <>
            <Dialog
                maxWidth={false}
                fullWidth={true}
                open={open}
                PaperProps={{
                    style: {
                        width: '600px',
                        minHeight: '50vh',
                    },
                }}
            >
                <DialogTitle>
                    {isEdit ? t('update_solution', {ns: ['headers']}) : t('add_new_solution', {ns: ['headers']})}
                </DialogTitle>
                <DialogContent dividers>
                    <div>
                        <Container sx={{minHeight: '40vh'}}>
                            {getStepContent(activeStep)}
                        </Container>
                        <Stepper activeStep={activeStep}>
                            {steps.map((label, index) => (
                                <Step key={label} onClick={() => setActiveStep(index)}>
                                    <StepLabel>{label}</StepLabel>
                                </Step>
                            ))}
                        </Stepper>
                    </div>
                </DialogContent>
                <DialogActions>
                    <Button autoFocus onClick={handleCancel}>
                        {t('button_label.cancel', {ns: ['dialogs']})}
                    </Button>
                    <Button
                        onClick={() => (activeStep > 0 ? setActiveStep(activeStep - 1) : setActiveStep(activeStep))}
                    >
                        {t('button_label.back', {ns: ['dialogs']})}
                    </Button>
                    {activeStep !== steps.length - 1 ? (
                        <Button
                            onClick={() =>
                                activeStep < steps.length - 1 ? setActiveStep(activeStep + 1) : setActiveStep(activeStep)
                            }
                        >
                            {t('button_label.next', {ns: ['dialogs']})}
                        </Button>
                    ) : (
                        <Button onClick={() => {
                            let x = isSubmittable()
                            setShowInvalidInput(!x.validInput)
                            if (x.validInput) {
                                send();
                            }

                        }}>{t('button_label.send', {ns: ['dialogs']})}</Button>
                    )}
                    <Backdrop
                        sx={{color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1}}
                        open={openBackDrop}
                        onClick={handleCloseBackDrop}
                    >
                        <CircularProgress color="inherit"/>
                    </Backdrop>
                </DialogActions>
            </Dialog>
            <Dialog
                open={showInvalidInput}
                onClose={() => setShowInvalidInput(false)}
            >
                <DialogTitle>Warning</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {isSubmittable().message}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setShowInvalidInput(false)} color="primary">
                        {t('okay', {ns: ['dialogs']})}
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog
                open={showWarningNotValidConfig}
                onClose={() => setShowWarningNotValidConfig(false)}
            >
                <DialogTitle>Warning</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Your configuration is invalid, if you dont fix it, your custom values will not be used
                    </DialogContentText>
                </DialogContent>
                <DialogActionComponent
                    onCancel={() => setShowWarningNotValidConfig(false)}
                    onConfirm={handleConfirmSubmit}
                    cancelText={t('button_label.cancel', {ns: ['dialogs']})}
                    confirmText={t('button_label.start', {ns: ['dialogs']})}
                />
            </Dialog>
        </>
    );
};

