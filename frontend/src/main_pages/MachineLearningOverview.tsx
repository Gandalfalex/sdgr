import {Grid, List, ListItem, ListItemButton, ListItemText} from "@mui/material";
import React, {useEffect, useState} from "react";
import {Model} from "../typedefs/django_types";
import {getMlModels} from "../api/DjangoAPI";
import {useNavigate} from "react-router-dom";
import {DataHeaderGridComponent} from "../Components/shared_components/grids/DataHeaderGridComponent";
import {DataGridComponent} from "../Components/shared_components/grids/DataGridComponent";
import {DataOverviewBox} from "../Components/shared_components/boxes/DataOverviewBox";
import {useTranslation} from "react-i18next";
import {useSnackbar} from "../Components/shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../typedefs/error_types";


export const MachineLearningOverview = () => {
    const [mlModels, setMlModels] = useState<Array<Model>>([])
    const navigate = useNavigate();
    const {t} = useTranslation(['headers', 'errors']);
    const {showMessage} = useSnackbar();

    useEffect(() => {
        getMlModels().then(res => {
            return setMlModels(res);
        }).catch(error => {
            showMessage(t(error.response.data.i18nKey, {ns: ['errors']}), SnackbarSeverity.ERROR)
        })
    }, []);

    return (
        <DataGridComponent>
            <DataHeaderGridComponent header={t('ml_models', {ns: ['headers']})}/>
            {mlModels && mlModels.length === 0 ? <div/> :
                <Grid item xs={8}>
                    <DataOverviewBox>
                        <List
                            sx={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: 'column',
                            }}>
                            {mlModels.map((mlModel) => (
                                <ListItem key={mlModel.id} sx={{
                                    m: 0,
                                    p: 0,
                                }}>
                                    <ListItemButton onClick={() => {
                                        navigate(`/ml/${mlModel.id}`);
                                    }
                                    }>
                                        <ListItemText primary={mlModel.name}/>
                                        {mlModel.description}
                                    </ListItemButton>
                                </ListItem>
                            ))}
                        </List>
                    </DataOverviewBox>
                </Grid>
            }
        </DataGridComponent>
    );
}



