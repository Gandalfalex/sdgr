import {Avatar, Box, IconButton, ListItemIcon, Menu, MenuItem, Tooltip} from "@mui/material";
import {Logout, Settings} from "@mui/icons-material";
import React, {useMemo, useState} from "react";
import {useTranslation} from "react-i18next";
import {getUser} from "../../api/SpringAPI";
import {User} from "../../typedefs/spring_types";
import {useNavigate} from "react-router-dom";
import {Simulate} from "react-dom/test-utils";
import error = Simulate.error;

export const UserDataViewComponent = () => {

    const [personMenuAnchors, setPersonMenuAnchors] = useState<any>(null)
    const [open, setOpen] = useState(false);
    const {t} = useTranslation(['dialogs']);
    const [user, setUser] = useState<User>()
    const navigate = useNavigate();
    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setOpen(true)
        setPersonMenuAnchors(event.currentTarget)
    }
    const handleClose = () => {
        setOpen(false);
        setPersonMenuAnchors(null)
    }

    useMemo(() => {
        getUser().then(res => {
            setUser(res);
        }).catch(error => {
            console.error("API call failed:", error);
        })
    }, []);

    const handleLogOut = () => {
        sessionStorage.clear()
        setOpen(false);
        setPersonMenuAnchors(null)
        navigate('/login');
    }

    return (<div>
            <Box sx={{display: 'flex', alignItems: 'center', textAlign: 'center'}}>
                <Tooltip title="Account settings">
                    <IconButton
                        onClick={handleClick}
                        size="small"
                        sx={{ml: 2}}
                        aria-controls={open ? 'account-menu' : undefined}
                        aria-haspopup="true"
                        aria-expanded={open ? 'true' : undefined}
                    >
                        <Avatar sx={{width: 40, height: 40}}>{user?.name.charAt(0).toUpperCase()}</Avatar>
                    </IconButton>
                </Tooltip>
            </Box>
            <Menu
                anchorEl={personMenuAnchors}
                id="account-menu"
                open={open}
                onClose={handleClose}
                onClick={handleClose}
                PaperProps={{
                    elevation: 0,
                    sx: {
                        overflow: 'visible',
                        filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                        mt: 1.5,
                        '& .MuiAvatar-root': {
                            width: 32,
                            height: 32,
                            ml: -0.5,
                            mr: 1,
                        },
                        '&:before': {
                            content: '""',
                            display: 'block',
                            position: 'absolute',
                            top: 0,
                            right: 14,
                            width: 10,
                            height: 10,
                            bgcolor: 'background.paper',
                            transform: 'translateY(-50%) rotate(45deg)',
                            zIndex: 0,
                        },
                    },
                }}
                transformOrigin={{horizontal: 'right', vertical: 'top'}}
                anchorOrigin={{horizontal: 'right', vertical: 'bottom'}}
            >

                <MenuItem onClick={handleClose}>
                    <ListItemIcon>
                        <Settings fontSize="small"/>
                    </ListItemIcon>
                    Settings
                </MenuItem>
                <MenuItem onClick={handleLogOut}>
                    <ListItemIcon>
                        <Logout fontSize="small"/>
                    </ListItemIcon>
                    {t('button_label.logout', {ns: ['dialogs']})}
                </MenuItem>
            </Menu>
        </div>
    );
}