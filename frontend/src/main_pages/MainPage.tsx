import React from "react";
import '../css/split-screen.css'
import tsaImage
    from "../image/tsa_training.png"
import mlImage
    from "../image/model_train.png"
import projectImage
    from "../image/timeline.png"
import {Stack} from "@mui/system";
import {Paper, Typography} from "@mui/material";
import { useTranslation} from "react-i18next";

export const MainPage = () => {
    const { t } = useTranslation(['main_page']);

    return (
        <Paper sx={{width: '70%'}}>
            <Stack direction={"column"} overflow={"auto"} height={"100vh"} paddingTop={"10vh"}>

                <Stack direction={"row"}>
                    <div className="column-one">
                        <Typography variant="h4" gutterBottom>Project</Typography>
                        {t("project_info", {ns: ['main_page']})}
                    </div>
                    <div className="column-two">
                        <img src={projectImage} alt="Description"/>
                    </div>
                </Stack>

                <Stack direction={"row"}>
                    <div className="column-two">
                        <img src={mlImage} alt="Description"/>
                    </div>
                    <div className="column-one">
                        <Typography variant="h4" gutterBottom>Machine Learning</Typography>
                        {t('ml_info', {ns: ['main_page']})}
                    </div>
                </Stack>

                <Stack direction={"row"}>
                    <div className="column-one">
                        <Typography variant="h4" gutterBottom>Time Series Analysis</Typography>
                        {t("tsa_info", {ns: ['main_page']})}
                    </div>
                    <div className="column-two">
                        <img src={tsaImage} alt="Description"/>
                    </div>
                </Stack>
            </Stack>
        </Paper>
    );
}