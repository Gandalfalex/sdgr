import {Box, Card, CardContent, CardHeader, Typography,} from "@mui/material";
import React, {useEffect, useState} from "react";
import {getLogSessionGraph, getLogSessions} from "../../../api/SpringAPI";
import {LogDataGraph, LogSession} from "../../../typedefs/spring_types";
import LogGraphElement from '../../graphs/LogGraphElement';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, {SelectChangeEvent} from '@mui/material/Select';

interface logGraphProps {
    trackId: number,
}

export const LogGraphChooserElement = (props: logGraphProps) => {
    const {trackId} = props;
    const [sessions, setSessions] = useState<Array<LogSession>>([]);
    const [graphData, setGraphData] = useState<LogDataGraph>();
    const [sessionSelect, setSelectSession] = React.useState<string>("");

    const handleOpenLogGraph = (sessionValue: string) => {
        if (sessionValue !== null || sessionValue !== "") {
            getLogSessionGraph(trackId, sessionValue).then(res => setGraphData(res));
        }
    }

    const [open, setOpen] = React.useState(false);

    const handleChange = (event: SelectChangeEvent<string>) => {
        setSelectSession(event.target.value);
        handleOpenLogGraph(event.target.value);
    };

    const handleClose = () => {
        setOpen(false);
    };

    const handleOpen = () => {
        setOpen(true);
    };


    useEffect(() => {
        getLogSessions(trackId).then(res => setSessions(res));
    }, [trackId])
    return (
        <Box
            sx={{
                display: 'inline-block',
                m: 1,
                height: "100%",
                width: "100%",
            }}
        >
            <Card sx={{display: "inline-block", width: '95%'}}>
                <CardHeader title="Graph"/>
                <CardContent>
                    <FormControl sx={{m: 1, minWidth: 200,}}>

                        {sessions.length ?
                            <Box sx={{
                                display: 'inline-block',
                                m: 1,
                                height: "100%",
                                width: "100%",
                            }}>
                                <InputLabel id="controlled-open-select-label">Session</InputLabel>
                                <Select
                                    labelId="controlled-open-select-label"
                                    id="controlled-open-select"
                                    open={open}
                                    onClose={handleClose}
                                    onOpen={handleOpen}
                                    value={sessionSelect}
                                    onChange={handleChange}
                                    fullWidth
                                    size="small"
                                >
                                    {sessions
                                        .map((row) => (
                                            <MenuItem value={row.session}>
                                                {row.session}
                                            </MenuItem>
                                        ))}
                                </Select>
                            </Box>
                            : <Box
                                sx={{display: 'flex', alignItems: 'center', justifyContent: 'center', height: '300px'}}>
                                <Typography align="center" fontSize={25}>No Sessions has been recorded</Typography>
                            </Box>}
                    </FormControl>
                    <Box sx={{display: "inline-block", height: "100%", width: "100%"}}>
                        <LogGraphElement data={graphData}/>
                    </Box>
                </CardContent>
            </Card>
        </Box>)
}
