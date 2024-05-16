import {Box, createTheme, ThemeProvider} from "@mui/material";
import {BrowserRouter, Navigate, Route, Routes} from "react-router-dom";
import {MainPage} from "./main_pages/MainPage";
import {MLAlgorithm} from "./Components/machineLearning/MLAlgorithm";
import {LogInPage} from "./main_pages/LogInPage";
import {TSDAlgorithm} from "./Components/time_series_composition/TSDAlgorithm";
import React from "react";
import {SnackbarProvider} from "./Components/shared_components/snackbar/SnackbarProvider";
import {WebSocketProvider} from "./Components/websockets/WebSocketProvider";
import {TimeSeriesCompositionOverview} from "./main_pages/TimeSeriesCompositionOverview";
import {MachineLearningOverview} from "./main_pages/MachineLearningOverview";
import {DataSetViewer} from "./main_pages/DataSetViewer";
import {UserSurvey} from "./main_pages/UserSurvey";
import {ActionBarComponent} from "./main_pages/ActionBarCompoent";
import WebSocketMessagesDrawerComponent from "./Components/websockets/WebSocketDrawerComponent";
import {ProjectOverview} from "./Components/project/ProjectOverview";
import OpenProjects from "./main_pages/OpenProjects";
import {DocumentationPage} from "./main_pages/DocumentationPage";


function App() {

    const theme = createTheme({
        palette: {
            mode: 'light',
            primary: {
                main: '#133259',
                light: '#235ca5',
            },
            secondary: {
                main: '#0a9735',
                light: '#d9d9d4',
            },
        },
    });


    return (
        <ThemeProvider theme={theme}>
            <SnackbarProvider>
                <Box
                    className={'gradientBackground'}
                    bgcolor={theme.palette.primary.light}
                    width={'100%'}
                    height={'100vh'}
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    overflow={'hidden'}
                >
                        <BrowserRouter>

                            <Routes>
                                <Route path='/login' element={<LogInPage/>} />
                                <Route path='*' element={

                                    <WebSocketProvider>
                                        <ActionBarComponent/>
                                        <Routes>
                                            <Route path='/' element={<ProtectedRoute><MainPage/></ProtectedRoute>}/>
                                            <Route path='/ml'
                                                   element={<ProtectedRoute><MachineLearningOverview/></ProtectedRoute>}/>
                                            <Route path='/tsd'
                                                   element={<ProtectedRoute><TimeSeriesCompositionOverview/></ProtectedRoute>}/>
                                            <Route path='/ml/:mlId' element={<ProtectedRoute><MLAlgorithm/></ProtectedRoute>}/>
                                            <Route path='/tsd/:tsdId' element={<ProtectedRoute><TSDAlgorithm/></ProtectedRoute>}/>
                                            <Route path='/project/:projectId'
                                                   element={<ProtectedRoute><ProjectOverview/></ProtectedRoute>}/>
                                            <Route path='/project' element={<ProtectedRoute><OpenProjects/></ProtectedRoute>}/>
                                            <Route path='/traindata' element={<ProtectedRoute><DataSetViewer/></ProtectedRoute>}/>
                                            <Route path='/survey' element={<ProtectedRoute><UserSurvey/></ProtectedRoute>}/>
                                            <Route path="/documentation"
                                                   element={<ProtectedRoute><DocumentationPage/></ProtectedRoute>}/>
                                        </Routes>
                                        <WebSocketMessagesDrawerComponent/>
                                    </WebSocketProvider>
                                }/>
                            </Routes>

                        </BrowserRouter>

                </Box>
            </SnackbarProvider>
        </ThemeProvider>
    );
}

type ProtectedRouteProps = {
    children: React.ReactNode;
};

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({children}) => {
    const jwtToken = sessionStorage.getItem('jwt');
    if (jwtToken) {
        return <>{children}</>;
    }
    return <Navigate to="/login"/>;
};

export default App;