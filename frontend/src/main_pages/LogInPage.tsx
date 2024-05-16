import React, {useState} from 'react';
import {Container, Paper, Typography} from '@mui/material';
import {useNavigate} from "react-router-dom";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import LogInForm from "../Components/security/LogInForm";
import {SignUpForm} from "../Components/security/SignUpForm";
import CustomSnackbar from "../Components/shared_components/snackbar/CustomSnackBar";
import {SnackbarSeverity} from "../typedefs/error_types";
import {useSnackbar} from "../Components/shared_components/snackbar/SnackbarContext";
import {useTranslation} from "react-i18next";


export const LogInPage = () => {
    const navigate = useNavigate();
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [activeTab, setActiveTab] = useState(0);
    const {showMessage} = useSnackbar();
    const { t } = useTranslation(['components']);
    const handleSnackbarClose = () => {
        setSnackbarOpen(false);
    };


    const handleChangeTab = (event: any, newValue: any) => {
        setActiveTab(newValue);
    };


    const handleDialogClose = (closedByUser: boolean) => {
        if (closedByUser) {
            navigate("/")
            window.location.reload();
        }
    };

    const handleDialogError = (hadError: boolean) => {
        if (hadError) {
            setSnackbarOpen(true);
        } else {
            navigate("/")
        }
    };

    return (
        <Container component="main" maxWidth="xs">
            <Paper elevation={3}
                   style={{padding: '2rem', display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
                <Typography variant="h5">{t('login', {ns: ['components']})}</Typography>
                <Tabs value={activeTab} onChange={handleChangeTab} aria-label="login-signup-tabs">
                    <Tab label={t('login', {ns: ['components']})}/>
                    <Tab label={t('signup', {ns: ['components']})}/>
                </Tabs>

                {activeTab === 0 && (
                    <LogInForm onClose={handleDialogClose} onError={handleDialogError}/>
                )}
                {activeTab === 1 && (
                    <SignUpForm onClose={handleDialogClose} onError={handleDialogError}/>
                )}
                <CustomSnackbar
                    open={snackbarOpen}
                    onClose={handleSnackbarClose}
                    severity={SnackbarSeverity.ERROR}
                    message="Login Failed"
                />
            </Paper>
        </Container>
    );
}