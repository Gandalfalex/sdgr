import {alpha, styled} from '@mui/material/styles';
import InputBase from "@mui/material/InputBase";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import SearchIcon from "@mui/icons-material/Search";
import React from "react";
import {useTranslation} from "react-i18next";

interface SearchBarProps {
    searchQuery: string;
    handleSearchQuery: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

const Search = styled('div')(({theme}) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
        marginLeft: theme.spacing(1),
        width: 'auto',
    },
}));

const SearchIconWrapper = styled('div')(({theme}) => ({
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
}));

const StyledInputBase2 = styled(InputBase)(({theme}) => ({
    color: 'inherit',
    '& .MuiInputBase-input': {
        padding: theme.spacing(1, 1, 1, 0),

        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create('width'),
    },
}));

export const SearchBarComponent = (props: SearchBarProps) => {
    const {searchQuery, handleSearchQuery} = props;
    const {t} = useTranslation(['components']);

    return (
        <AppBar position="static">
            <Toolbar>
                <Search>
                    <SearchIconWrapper>
                        <SearchIcon/>
                    </SearchIconWrapper>
                    <StyledInputBase2
                        placeholder={t('search', {ns: ['components']})}
                        inputProps={{'aria-label': 'search'}}
                        onChange={handleSearchQuery}
                        value={searchQuery}
                    />
                </Search>
            </Toolbar>
        </AppBar>
    )
}
