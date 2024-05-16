import {Grid, List, ListItem, ListItemButton, ListItemText} from "@mui/material";
import {useEffect, useState} from "react";
import {getTsdModels} from "../api/DjangoAPI";
import {useNavigate} from "react-router-dom";
import {Model} from "../typedefs/django_types";
import {DataGridComponent} from "../Components/shared_components/grids/DataGridComponent";
import {DataHeaderGridComponent} from "../Components/shared_components/grids/DataHeaderGridComponent";
import {DataOverviewBox} from "../Components/shared_components/boxes/DataOverviewBox";
import {useTranslation} from "react-i18next";
import {SnackbarSeverity} from "../typedefs/error_types";
import {useSnackbar} from "../Components/shared_components/snackbar/SnackbarContext";


export const TimeSeriesCompositionOverview = () => {
    const [tsdModels, setTsdModels] = useState<Array<Model>>([])
    const navigate = useNavigate();
    const { t } = useTranslation(['dialogs', 'headers','errors']);
    const {showMessage} = useSnackbar();

    useEffect(() => {
        getTsdModels().then(res => {
            return setTsdModels(res);
        }).catch(error => {
            showMessage(t(error.response.data.i18nKey, {ns: ['errors']}), SnackbarSeverity.ERROR)
        })
    }, []);

    return (
        <DataGridComponent>
            <DataHeaderGridComponent header={t('tsa_models', {ns: ['headers']})}/>
            {tsdModels.length === 0 ? <div/> :
                <Grid item xs={8}>
                    <DataOverviewBox>
                        <List
                            sx={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: 'column',
                            }}>
                            {tsdModels.map((tsdModel) => (
                                <ListItem key={tsdModel.id} sx={{
                                    m: 0,
                                    p: 0,
                                }}>
                                    <ListItemButton onClick={() => {
                                        navigate(`/tsd/${tsdModel.id}`);
                                    }
                                    }>
                                        <ListItemText primary={tsdModel.name}/>
                                        {tsdModel.description}
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

