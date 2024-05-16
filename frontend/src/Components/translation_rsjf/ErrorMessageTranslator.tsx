import {useTranslation} from 'react-i18next';
import {RSJFError} from "../../typedefs/error_types";

export function useErrorMessageConverter() {
    const {t} = useTranslation(['schemas']);

    function convertError(error: RSJFError): string {
        const i18nKey = `errors.${error.name}`;
        return t(i18nKey, error.params)
    }

    return convertError;
}