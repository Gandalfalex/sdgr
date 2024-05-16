import {Card, CardHeader, Collapse, useTheme} from "@mui/material";
import React, {useEffect, useState} from "react";
import {Track} from "../../../typedefs/spring_types";
import {deleteTrack, editTrack} from "../../../api/SpringAPI";
import {TrackDialog} from "../../dialogs/TrackDialog";
import CardTabPanel from "./dataset/skeletons/CardTabPanel";
import {OptionsMenu} from "../../shared_components/OptionsMenu";

interface TrackElementProps {
    projectId: number,
    track: Track,
    expanded: boolean,
    handleExpandClick: (id: number | null) => void,
    refreshTracks: () => void
}

export const TrackElement = (props: TrackElementProps) => {

    const {projectId, track, expanded, handleExpandClick, refreshTracks} = props;
    const theme = useTheme();
    const [showEditTrackDialog, setShowEditTrackDialog] = useState(false);

    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const handleTrackDelete = () => {
        handleMenuClose();
        deleteTrack(projectId, track.id).then(() => {
            refreshTracks();
        });
    }


    const handleCloseEditTrackDialog = (editedTrack?: Track) => {
        setShowEditTrackDialog(false);

        if (editedTrack) {
            editTrack(projectId, track.id, editedTrack).then(() => refreshTracks());
        }
    }


    useEffect(() => {
    }, [])  // eslint-disable-line react-hooks/exhaustive-deps
    return (
        <Card sx={{backgroundColor: theme.palette.secondary.light}}>
            <CardHeader
                subheader={
                    <div style={{userSelect: 'none'}}>
                        repeating: {track.repeating ? "True" : "False"}
                    </div>
                }
                titleTypographyProps={{variant: 'h6'}}
                action={
                    // TODO Delete dialog
                    <OptionsMenu
                        value={track}
                        setShowEditDialog={setShowEditTrackDialog}
                        setShowDeleteDialog={handleTrackDelete}
                    />
                }
            />
            <Collapse in={expanded} timeout="auto" unmountOnExit>
                <CardTabPanel projectId={projectId} track={track} refreshTracks={refreshTracks}/>
            </Collapse>
            <TrackDialog id="new-track" isEdit keepMounted open={showEditTrackDialog}
                         onClose={handleCloseEditTrackDialog} value={track}/>
        </Card>
    );
}
