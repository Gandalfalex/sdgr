import React, {useState} from 'react';
import {Button, TextField} from '@mui/material';
import {signupUser} from "../../api/ApiConnector";
import {useTranslation} from "react-i18next";
import {SnackbarSeverity} from "../../typedefs/error_types";
import {useSnackbar} from "../shared_components/snackbar/SnackbarContext";

type DialogCallback = (flag: boolean) => void;

type LoginDialogProps = {
    onClose: DialogCallback;
    onError: DialogCallback;
};
export const SignUpForm: React.FC<LoginDialogProps> = ({onClose, onError}) => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const {t} = useTranslation(['components', 'errors']);
    const {showMessage} = useSnackbar();
    const handleSignUp = (event: any) => {
        event.preventDefault();

        signupUser(email, password, firstName, lastName)
            .then(res => {
                sessionStorage.setItem('jwt', res.token);
                onClose(true);
            })
            .catch(error => {
                showMessage(t(error.response.data.i18nKey, {ns: ['errors']}), SnackbarSeverity.ERROR)
            });
    };

    return (
        <div>
            <form onSubmit={handleSignUp}>
                <TextField
                    value={firstName}
                    onChange={e => setFirstName(e.target.value)}
                    fullWidth margin="normal" label={t('login_f_name', {ns: ['components']})} variant="outlined"/>
                <TextField
                    value={lastName}
                    onChange={e => setLastName(e.target.value)}
                    fullWidth margin="normal" label={t('login_s_name', {ns: ['components']})} variant="outlined"/>
                <TextField
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    fullWidth margin="normal" label={t('login_e_mail', {ns: ['components']})} type="email"
                    variant="outlined"/>
                <TextField
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    fullWidth margin="normal" label={t('login_pass', {ns: ['components']})} type="password"
                    variant="outlined"/>
                <Button type="submit" variant="contained" color="primary">
                    {t('sign_up', {ns: ['components']})}
                </Button>
            </form>
        </div>
    );
}

