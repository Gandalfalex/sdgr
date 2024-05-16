import {useState} from "react";
import {SnackbarSeverity} from "../../../typedefs/error_types";
import CustomSnackbar from "./CustomSnackBar";
import SnackbarContext from "./SnackbarContext";

interface SnackbarProviderProps {
    children: React.ReactNode;
}

export const SnackbarProvider: React.FC<SnackbarProviderProps> = ({children}) => {
    const [snackbarOpen, setSnackbarOpen] = useState<boolean>(false);
    const [snackBarMessage, setSnackbarMessage] = useState<string>("");
    const [snackBarSeverity, setSnackBarSeverity] = useState<SnackbarSeverity>(SnackbarSeverity.ERROR);

    const showMessage = (message: string, severity: SnackbarSeverity) => {
        setSnackbarMessage(message);
        setSnackBarSeverity(severity);
        setSnackbarOpen(true);
    };

    return (
        <SnackbarContext.Provider value={{showMessage}}>
            {children}
            <CustomSnackbar
                open={snackbarOpen}
                onClose={() => setSnackbarOpen(false)}
                severity={snackBarSeverity}
                message={snackBarMessage}
            />
        </SnackbarContext.Provider>
    );
};