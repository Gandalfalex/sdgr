import React from 'react';
import {Accordion, AccordionDetails, AccordionSummary, Typography} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';


interface GenericAccordionProps {
    header: string;
    details: React.ReactNode;
    expanded: boolean;
    onChange: () => void;
}

const GenericAccordion: React.FC<GenericAccordionProps> = ({header, details, expanded, onChange}) => {
    return (
        <Accordion expanded={expanded} onChange={onChange}>
            <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                <Typography>{header}</Typography>
            </AccordionSummary>
            <AccordionDetails>
                {details}
            </AccordionDetails>
        </Accordion>
    );
};

export default GenericAccordion;
