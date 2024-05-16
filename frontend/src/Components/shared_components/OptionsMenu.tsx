import React, {useState} from 'react';
import {IconButton, Menu, MenuItem} from "@mui/material";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import {useTranslation} from "react-i18next";

interface OptionsMenuProps {
    value: any;
    setShowEditDialog?: React.Dispatch<React.SetStateAction<boolean>>;
    setShowDeleteDialog?: React.Dispatch<React.SetStateAction<boolean>>;
    setShowCopyDialog?: React.Dispatch<React.SetStateAction<boolean>>;
}

export const OptionsMenu: React.FC<OptionsMenuProps> = ({
                                                            value,
                                                            setShowEditDialog,
                                                            setShowDeleteDialog,
                                                            setShowCopyDialog
                                                        }) => {
    const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
    const {t} = useTranslation(['dialogs']);
    const openMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorEl(event.currentTarget);
    };


    const closeMenu = () => {
        setAnchorEl(null);
    };

    return (
        <>
            <IconButton onClick={openMenu}>
                <MoreVertIcon/>
            </IconButton>
            <Menu
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={closeMenu}>

                {setShowEditDialog
                    ? <MenuItem onClick={() => {
                        if (value) {
                            setShowEditDialog(true);
                        }
                        closeMenu();
                    }}>
                        {t('button_label.update', {ns: ['dialogs']})}
                    </MenuItem>
                    : null
                }
                {setShowCopyDialog
                    ? <MenuItem onClick={() => {
                        if (value) {
                            setShowCopyDialog(true);
                        }
                        closeMenu();
                    }}>
                        {t('button_label.copy', {ns: ['dialogs']})}
                    </MenuItem>
                    : null
                }
                {setShowDeleteDialog
                    ? <MenuItem onClick={() => {
                        setShowDeleteDialog(true);
                        closeMenu();
                    }}>
                        {t('button_label.delete', {ns: ['dialogs']})}
                    </MenuItem>
                    : null
                }
            </Menu>
        </>
    );
};
