import {useState} from "react";
import {
    Button,
    FormControl,
    FormControlLabel,
    FormLabel,
    Paper,
    Radio,
    RadioGroup,
    Step,
    StepLabel,
    Stepper,
    TextField,
    Typography
} from '@mui/material';
import {LargeInformationPaperComponent} from "../Components/shared_components/paper/LargeInformationPaperComponent";
import {postSurvey} from "../api/DjangoAPI";
import {useSnackbar} from "../Components/shared_components/snackbar/SnackbarContext";
import {SnackbarSeverity} from "../typedefs/error_types";
import {useNavigate} from "react-router-dom";
import {useTranslation} from "react-i18next";

export const UserSurvey = () => {
    // Initialize state for each question
    const [answers, setAnswers] = useState(Array(20).fill(0));
    const [activeStep, setActiveStep] = useState(0);
    const [userInfo, setUserInfo] = useState({});
    const {showMessage} = useSnackbar();
    const navigate = useNavigate();
    const { t } = useTranslation(['survey', 'dialogs']);


    const handleUserInfoChange = (field: keyof typeof userInfo, value: string) => {
        setUserInfo({...userInfo, [field]: value});
    };

    const stepQuestions = [
        {
            header: "header_usability",
            steps: 6,
            questions: [
                { code: 1, text: "key_usability_regular_use" },
                { code: 1, text: "key_usability_complicated" },
                { code: 1, text: "key_usability_easy_to_use" },
                { code: 1, text: "key_usability_need_support" },
                { code: 1, text: "key_usability_well_integrated" },
                { code: 1, text: "key_usability_inconsistent" },
                { code: 1, text: "key_usability_easy_learning" },
                { code: 1, text: "key_usability_cumberstone" },
                { code: 1, text: "key_usability_confident" },
                { code: 1, text: "key_usability_learn_a_lot" },
            ]
        },
        {
            header: "header_stressful",
            steps: 10,
            questions: [
                { code: 1, text: "key_stressful_mental_demand" },
                { code: 1, text: "key_stressful_physical_demand" },
                { code: 1, text: "key_stressful_pace" },
                { code: 1, text: "key_stressful_success" },
                { code: 1, text: "key_stressful_workload" },
                { code: 1, text: "key_stressful_emotions" },
            ]
        },
        {
            header: "header_personal_info",
            steps: 10,
            questions: [
                { code: 2, text: "key_personal_age", type: "input" },
                { code: 2, text: "key_personal_background", type: "input" },
                { code: 3, text: "key_personal_technical_affinity"},
                { code: 2, text: "key_personal_experience", type: "input" },
                { code: 2, text: "key_personal_notes", type: "input" },
                { code: 2, text: "key_personal_task", type: "input" }
            ]
        }
    ];



    const handleSubmit = () => {
        const data = {
            userInformation: userInfo,
            mentalLoad: answers.slice(0, 10).reduce((acc, val, idx) => ({...acc, [idx + 1]: val}), {}),
            userFeeling: answers.slice(10, 20).reduce((acc, val, idx) => ({...acc, [idx + 1]: val}), {})
        };
        postSurvey(data).then(res => showMessage("Thanks", SnackbarSeverity.SUCCESS));
        navigate('/');
    };

    const handleNext = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    // Update answers state
    const handleChange = (questionIndex: number, value: string) => {
        const newAnswers = [...answers];
        newAnswers[questionIndex] = value;
        setAnswers(newAnswers);
    };

    const handleUserChange = (field: keyof typeof userInfo, value: string) => {
        setUserInfo({...userInfo, [field]: value});
    };

    const createRadioButtons = (numOptions: number) => {
        let radioButtons = [];
        for (let i = 0; i < numOptions; i++) {
            radioButtons.push(<FormControlLabel key={i} value={i.toString()} control={<Radio/>} label={i.toString()}/>);
        }
        return radioButtons;
    };


    const renderQuestion = (question: any, index: number, activeStep: number) => {
        switch (question.code) {
            case 1: // For radio button questions
                return (
                    <FormControl key={index + (activeStep * 10)}>
                        <FormLabel id={`question-label-${index + (activeStep * 10)}`}>{t(question.text, {ns: ['survey']})}</FormLabel>
                        <RadioGroup
                            row
                            aria-labelledby={`question-label-${index + (activeStep * 10)}`}
                            name={`question-${index + (activeStep * 10)}`}
                            value={answers[index + (activeStep * 10)]}
                            onChange={(e) => handleChange(index + (activeStep * 10), e.target.value)}
                        >
                            {createRadioButtons(stepQuestions[activeStep].steps)}
                        </RadioGroup>
                    </FormControl>
                );
            case 2:
                const fieldName = question.text.toLowerCase().replace(/ /g, '') as keyof typeof userInfo;
                return (
                    <TextField
                        key={index}
                        label={t(question.text, {ns: ['survey']})}
                        variant="outlined"
                        multiline
                        value={userInfo[fieldName]}
                        onChange={(e) => handleUserInfoChange(fieldName, e.target.value)}
                        fullWidth
                        margin="normal"
                    />
                );
            case 3:
                let elementName = question.text.toLowerCase().replace(/ /g, '') as keyof typeof userInfo;
                return (
                    <FormControl key={index + (activeStep * 10)}>
                        <FormLabel id={`question-label-${index + (activeStep * 10)}`}>{t(question.text, {ns: ['survey']})}</FormLabel>
                        <RadioGroup
                            row
                            aria-labelledby={`question-label-${index + (activeStep * 10)}`}
                            name={`question-${index + (activeStep * 10)}`}
                            value={answers[index + (activeStep * 10)]}
                            onChange={(e) => handleUserChange(elementName, e.target.value)}
                        >
                            {createRadioButtons(stepQuestions[activeStep].steps)}
                        </RadioGroup>
                    </FormControl>
                );
            default:
                return null;
        }
    };

    return (
        <Paper elevation={2}>
            <Paper key={"header_key"} elevation={2}>
                {activeStep === stepQuestions.length ? (
                    <LargeInformationPaperComponent header={"All steps completed"}>
                        <Typography>{t('tfyp', {ns: ['survey']})}</Typography>
                        <Button onClick={handleSubmit} variant="outlined">{ t('button_label.send', {ns: ['dialogs']})}</Button>
                    </LargeInformationPaperComponent>
                ) : (
                    <LargeInformationPaperComponent header={t(stepQuestions[activeStep].header, {ns: ['survey']})}>
                        {stepQuestions[activeStep].questions.map((question, index) => (
                            renderQuestion(question, index, activeStep)
                        ))}
                    </LargeInformationPaperComponent>
                )}
            </Paper>

            <Stepper activeStep={activeStep} style={{marginTop: '30px'}}>
                {stepQuestions.map((_, index) => (
                    <Step key={index}>
                        <StepLabel>Step {index + 1}</StepLabel>
                    </Step>
                ))}
            </Stepper>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '10px' }}>
                <Button disabled={activeStep === 0} onClick={handleBack}>
                    {t('button_label.back', {ns: ['dialogs']})}
                </Button>
                <Button onClick={handleNext}>
                    {activeStep === stepQuestions.length - 1 ? t('button_label.finish', {ns: ['dialogs']}) : t('button_label.next', {ns: ['dialogs']})}
                </Button>
            </div>
        </Paper>
    );
};