import React from "react";
import {Box, Typography} from "@mui/material";
import Preview from "../../../../graphs/Preview";
import {PreviewData} from "../../../../../typedefs/spring_types";

interface OverviewProps {
    previewData: PreviewData | undefined;
}

export const PreviewDataContainer: React.FC<OverviewProps> = ({previewData}) => {

    return (
        <Box sx={{height: "100%", width: "100%"}}>
            {previewData?.values.length
                ? <Preview data={previewData!}/>
                : <Box sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '240px'
                }}>
                    <Typography align="center">Cannot provide a preview, please check your
                        data</Typography>
                </Box>
            }
        </Box>
    )
}

export default PreviewDataContainer;