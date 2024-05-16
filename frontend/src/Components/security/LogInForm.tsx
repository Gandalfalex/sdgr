import React, {useState} from 'react';
import {Button, TextField} from '@mui/material';
import {loginUser} from "../../api/ApiConnector";
import {useTranslation} from "react-i18next";
import {SnackbarSeverity} from "../../typedefs/error_types";

type DialogCallback = (flag: boolean) => void;

type LoginDialogProps = {
    onClose: DialogCallback;
    onError: DialogCallback;
};

export const LogInForm: React.FC<LoginDialogProps> = ({onClose, onError}) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { t } = useTranslation(['components', 'errors']);

    const handleLogin = (event: any) => {
        event.preventDefault(); // Prevent default form submission

        loginUser(email, password)
            .then(res => {
                console.log(res.token);
                sessionStorage.setItem('jwt', res.token);
                sessionStorage.setItem('refreshToken', res.refreshToken)
                onClose(true);
            })
            .catch(error => {
                console.log(error.response.data.i18nKey)
                onError(true)
                console.error(t(error.response.data.i18nKey, {ns: ['errors']}), SnackbarSeverity.ERROR);
            });
    };


    return (
        <div>
            <form onSubmit={handleLogin}>
                <TextField
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    fullWidth margin="normal" label={t('login_e_mail', {ns: ['components']})} type="email" variant="outlined"/>
                <TextField
                    value={password}
                    onChange={e => setPassword(e.target.value)}
                    fullWidth margin="normal" label={t('login_pass', {ns: ['components']})} type="password" variant="outlined"/>
                <Button type="submit" variant="contained" color="primary">
                    {t('login', {ns: ['components']})}
                </Button>
            </form>
        </div>
    );
}

export default LogInForm;