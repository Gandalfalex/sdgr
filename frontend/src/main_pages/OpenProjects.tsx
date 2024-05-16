import {
    Grid,
    IconButton,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Tooltip,
    useTheme
} from "@mui/material";
import AddIcon from '@mui/icons-material/Add';
import {useNavigate} from "react-router-dom";
import React, {useEffect, useState} from "react";
import {deleteProject, getAllProjects} from "../api/SpringAPI";
import {Projects} from "../typedefs/spring_types";
import NewProjectDialog from "../Components/dialogs/NewProjectDialog";
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import {DataGridComponent} from "../Components/shared_components/grids/DataGridComponent";
import {DataHeaderGridComponent} from "../Components/shared_components/grids/DataHeaderGridComponent";
import {DataOverviewBox} from "../Components/shared_components/boxes/DataOverviewBox";
import {useTranslation} from "react-i18next";

export const OpenProjects = () => {
    const navigate = useNavigate();
    const theme = useTheme();
    const [allProjects, setAllProjects] = useState<Projects>([])
    const [showNewProjectDialog, setShowNewProjectDialog] = useState(false);
    const {t} = useTranslation(['dialogs', 'headers']);
    const handleAddClick = () => {
        setShowNewProjectDialog(true);
    }

    const onClose = () => {
        setShowNewProjectDialog(false);
    }

    useEffect(() => {
        getAllProjects().then(message => {
            if (Array.isArray(message)) {
                setAllProjects(message);
            } else {
                console.log('Error: Expected getAllProjects to return an array but got', message);
            }
        });
    }, []);


    return (
        <DataGridComponent>
            <DataHeaderGridComponent header={t('project_models', {ns: ['headers']})}>
                <Grid item xs={3}>
                    <Tooltip title={t('new_project', {ns: ['dialogs']})} arrow>
                        <IconButton className={'growButton'} onClick={handleAddClick}
                                    sx={{
                                        color: theme.palette.background.paper,
                                        alignSelf: 'center'
                                    }}>
                            <AddIcon sx={{
                                fontSize: 'xx-large'
                            }}/>
                        </IconButton>
                    </Tooltip>
                </Grid>
            </DataHeaderGridComponent>
            {allProjects.length === 0 ? <div/> :
                <Grid item xs={8}>
                    <DataOverviewBox>
                        <List
                            sx={{
                                display: "flex",
                                justifyContent: "center",
                                alignItems: "center",
                                flexDirection: 'column',
                            }}>
                            {allProjects.map((project) => (
                                <ListItem key={project.id} sx={{
                                    m: 0,
                                    p: 0,
                                }}>
                                    <ListItemButton onClick={() => {
                                        navigate(`/project/${project.id}`);
                                    }
                                    }>
                                        <ListItemText primary={project.name}/>
                                        <ListItemIcon>
                                            {project.sending ? <Tooltip title={t('project_sending', {ns: ['dialogs']})}>
                                                <div className={"circle"}/>
                                            </Tooltip> : <div/>}
                                        </ListItemIcon>
                                    </ListItemButton>
                                    <ListItemIcon>
                                        <Tooltip title={t('delete_success', {ns: ['dialogs']})} arrow>
                                            <IconButton className={'growButton'} onClick={() => {
                                                deleteProject(project.id);
                                                window.location.reload();
                                                return false;
                                            }}>
                                                <DeleteForeverIcon/>
                                            </IconButton>
                                        </Tooltip>
                                    </ListItemIcon>
                                </ListItem>
                            ))}
                        </List>
                    </DataOverviewBox>
                </Grid>
            }
            <NewProjectDialog open={showNewProjectDialog} onClose={onClose}/>
        </DataGridComponent>

    );
}

export default OpenProjects;