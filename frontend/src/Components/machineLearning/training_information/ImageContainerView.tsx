import React from 'react';
import styled from 'styled-components';
import {Dialog} from "@mui/material";

const StyledImage = styled.img`
  width: 90%;
  height: 90%;
  position: relative;
`;

const ImageContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
  position: relative;
`;

const DialogImage = styled.img`
    transform: scale(1);
`;


type ImageDisplayProps = {
    base64Image: string;
};

export const ImageContainerView: React.FC<ImageDisplayProps> = ({ base64Image }) => {
    const [open, setOpen] = React.useState(false);

    const handleClickOpen = () => {
        setOpen(true);
    };

    const handleClose = () => {
        setOpen(false);
    };

    return (
        <ImageContainer>
            <StyledImage src={`data:image/png;base64,${base64Image}`} alt="Training Image" onClick={handleClickOpen} />
            <Dialog open={open} onClose={handleClose} maxWidth={"md"}>
                <DialogImage src={`data:image/png;base64,${base64Image}`} alt="Training Image in Dialog" />
            </Dialog>
        </ImageContainer>
    );
};
