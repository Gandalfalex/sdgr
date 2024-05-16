import {createContext, useContext} from 'react';
import {SnackbarSeverity} from "../../../typedefs/error_types";

interface SnackbarContextType {
    showMessage: (message: string, severity: SnackbarSeverity) => void;
}

const SnackbarContext = createContext<SnackbarContextType | undefined>(undefined);
export default SnackbarContext;
export const useSnackbar = () => {
    const context = useContext(SnackbarContext);
    if (!context) {
        throw new Error('useSnackbar must be used within a SnackbarProvider');
    }
    return context;
};
