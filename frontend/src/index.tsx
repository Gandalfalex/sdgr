import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import "./i18n"
import {SnackbarProvider} from "./Components/shared_components/snackbar/SnackbarProvider";
import {SnackbarAPIErrorProvider} from "./Components/shared_components/snackbar/SnackBarError";

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
document.title = "SuS";
root.render(
    <SnackbarAPIErrorProvider>
        <App/>
    </SnackbarAPIErrorProvider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
