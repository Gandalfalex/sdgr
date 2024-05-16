import React from 'react';
import {Box, Container, TextField} from "@mui/material";
import {useTranslation} from "react-i18next";

interface CustomTextFieldProps {
    valueName: string;
    valueDescription: string;
    onChangeName: (event: React.ChangeEvent<HTMLInputElement>) => void;
    onChangeDescription: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const InformationTextField: React.FC<CustomTextFieldProps> = ({
                                                                  valueName,
                                                                  onChangeName,
                                                                  valueDescription,
                                                                  onChangeDescription
                                                              }) => {
    const { t } = useTranslation(['components']);
    return (
        <Container style={{display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <Box width={1}>
                <TextField
                    required
                    fullWidth
                    value={valueName}
                    onChange={onChangeName}
                    variant="filled"
                    label={t('information_text_name', {ns: ['components']})}

                />
            </Box>

            <Box width={1} mt={2}>
                <TextField
                    fullWidth
                    multiline
                    rows={4}
                    value={valueDescription}
                    onChange={onChangeDescription}
                    variant="filled"
                    label={t('information_description', {ns: ['components']})}

                />
            </Box>
        </Container>
    );
}
