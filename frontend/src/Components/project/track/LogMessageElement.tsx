import {
    Box,
    Card,
    CardContent,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableFooter,
    TableHead,
    TablePagination,
    TableRow,
    useTheme,
} from "@mui/material";
import React, {useEffect, useState} from "react";
import IconButton from '@mui/material/IconButton';
import {getLogSize, getTrackLogs} from "../../../api/SpringAPI";
import {LogMessage} from "../../../typedefs/spring_types";
import FirstPageIcon from '@mui/icons-material/FirstPage';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';
import LastPageIcon from '@mui/icons-material/LastPage';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import SearchIcon from '@mui/icons-material/Search';
import {useDebounce} from 'usehooks-ts'
import {SearchBarComponent} from "../../shared_components/SearchBarComponent";
import {useTranslation} from "react-i18next";


interface logMessagePaginationProps {
    trackId: number,
}

interface TablePaginationActionsProps {
    count: number;
    page: number;
    rowsPerPage: number;
    onPageChange: (
        event: React.MouseEvent<HTMLButtonElement>,
        newPage: number,
    ) => void;
}

function TablePaginationActions(props: TablePaginationActionsProps) {
    const theme = useTheme();
    const {count, page, rowsPerPage, onPageChange} = props;

    const handleFirstPageButtonClick = (
        event: React.MouseEvent<HTMLButtonElement>,
    ) => {
        onPageChange(event, 0);
    };

    const handleBackButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page - 1);
    };

    const handleNextButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, page + 1);
    };

    const handleLastPageButtonClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        onPageChange(event, Math.max(0, Math.ceil(count / rowsPerPage) - 1));
    };

    return (
        <Box sx={{flexShrink: 0, ml: 2.5}}>
            <IconButton
                onClick={handleFirstPageButtonClick}
                disabled={page === 0}
                aria-label="first page"
            >
                {theme.direction === 'rtl' ? <LastPageIcon/> : <FirstPageIcon/>}
            </IconButton>
            <IconButton
                onClick={handleBackButtonClick}
                disabled={page === 0}
                aria-label="previous page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowRight/> : <KeyboardArrowLeft/>}
            </IconButton>
            <IconButton
                onClick={handleNextButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="next page"
            >
                {theme.direction === 'rtl' ? <KeyboardArrowLeft/> : <KeyboardArrowRight/>}
            </IconButton>
            <IconButton
                onClick={handleLastPageButtonClick}
                disabled={page >= Math.ceil(count / rowsPerPage) - 1}
                aria-label="last page"
            >
                {theme.direction === 'rtl' ? <FirstPageIcon/> : <LastPageIcon/>}
            </IconButton>
        </Box>
    );
}

export const LogMessageElement = (props: logMessagePaginationProps) => {
    const {trackId} = props;
    const [logMessage, setLogMessage] = useState<Array<LogMessage>>([]);
    const [logSize, setLogSize] = useState<number>(10);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const debouncedValue = useDebounce<string>(searchQuery, 300);
    const { t } = useTranslation(['components']);

    const handleChangePage = (
        event: React.MouseEvent<HTMLButtonElement> | null,
        newPage: number,
    ) => {
        getLogSize(trackId, searchQuery).then(res => setLogSize(res));
        getTrackLogs(trackId, rowsPerPage, newPage, searchQuery).then(res => setLogMessage(res));
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (
        event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
    ) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        getLogSize(trackId, searchQuery).then(res => setLogSize(res));
        getTrackLogs(trackId, parseInt(event.target.value), 0, searchQuery).then(res => setLogMessage(res));
        setPage(0);
    };

    const handleSearchQuery = (
        event: React.ChangeEvent<HTMLInputElement>
    ) => {
        setSearchQuery(event.target.value);
        // update list size of elements
        getTrackLogs(trackId, rowsPerPage, 0, event.target.value).then(res => setLogMessage(res));
        getLogSize(trackId, event.target.value).then(res => setLogSize(res));
    }


    useEffect(() => {
        getTrackLogs(trackId, rowsPerPage, page, searchQuery).then(res => setLogMessage(res));
        getLogSize(trackId, searchQuery).then(res => setLogSize(res));
    }, [debouncedValue])  // eslint-disable-line react-hooks/exhaustive-deps
    return (
        <Card>
            <CardContent>
                <AppBar position="static">
                    <Toolbar>
                        <Typography
                            variant="h6"
                            noWrap
                            component="div"
                            sx={{flexGrow: 1, display: {xs: 'none', sm: 'block'}, width: "400px"}}
                        >
                            Logs
                        </Typography>
                        <SearchBarComponent searchQuery={searchQuery} handleSearchQuery={handleSearchQuery}/>
                    </Toolbar>
                </AppBar>
                {logMessage.length ?
                    <TableContainer>
                        <Table sx={{minWidth: 500}} aria-label="custom pagination table" size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell>
                                        {t('log_message', {ns: ['components']})}
                                    </TableCell>
                                    <TableCell>
                                        {t('log_time', {ns: ['components']})}
                                    </TableCell>
                                    <TableCell>
                                        {t('log_session', {ns: ['components']})}
                                    </TableCell>
                                    <TableCell>
                                        {t('log_dataset', {ns: ['components']})}
                                    </TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {logMessage.map((row) => (
                                    <TableRow>
                                        <TableCell>
                                            {row.message}
                                        </TableCell>
                                        <TableCell>
                                            {row.time}
                                        </TableCell>
                                        <TableCell>
                                            {row.sendSession}
                                        </TableCell>
                                        <TableCell>
                                            {row.dataSetName}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                            <TableFooter>
                                <TableRow>
                                    <TablePagination
                                        rowsPerPageOptions={[10, 20, 50, 100, {label: 'All', value: -1}]}
                                        colSpan={2}
                                        count={logSize}
                                        rowsPerPage={rowsPerPage}
                                        page={page}
                                        SelectProps={{
                                            inputProps: {
                                                'aria-label': 'rows per page',
                                            },
                                            native: true,
                                        }}
                                        onPageChange={handleChangePage}
                                        onRowsPerPageChange={handleChangeRowsPerPage}
                                        ActionsComponent={TablePaginationActions}
                                    />
                                </TableRow>
                            </TableFooter>
                        </Table>
                    </TableContainer>
                    :
                    <Box sx={{display: 'flex', alignItems: 'center', justifyContent: 'center', height: '300px'}}>
                        <Typography align="center" fontSize={25}> {t('log_no_record', {ns: ['components']})}</Typography>
                    </Box>
                }
            </CardContent>
        </Card>
    );
};


