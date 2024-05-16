import {useState} from "react";
import {patchTSDConfiguration, postTSDConfiguration, uploadTrainingFiles} from "../DjangoAPI";
import {TSDConfig} from "../../typedefs/django_types";

export const useHandleTSDConfigAPI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | undefined>();

    const handleTSDConfigAPI = async (
        isEdit: boolean,
        value: TSDConfig,
        selectedItems: number[],
        selectedFiles: File[],
        selectedTrainFiles: number[],
        handleSuccess: (data: any) => void) => {

        setLoading(true);
        setError(undefined);
        try {
            let data = null
            if (selectedFiles.length > 0) {
                const res = await uploadTrainingFiles(selectedFiles);
                if (isEdit) {
                    data = await patchTSDConfiguration(value.tsd_model, value.id, value.name, value.description, [...selectedItems, ...res], selectedTrainFiles);
                } else {
                    data = await postTSDConfiguration(value.tsd_model, value.name, value.description, [...selectedItems, ...res], selectedTrainFiles);
                }
            } else {
                if (isEdit) {
                    data = await patchTSDConfiguration(value.tsd_model, value.id, value.name, value.description, selectedItems, selectedTrainFiles);
                } else {
                    data = await postTSDConfiguration(value.tsd_model, value.name, value.description, selectedItems, selectedTrainFiles);
                }
            }
            setLoading(false);
            return data;
        } catch (e) {
            setLoading(false);
            setError(e as Error);
            return undefined;
        }
    };

    return {
        handleTSDConfigAPI,
        loading,
        error,
    };
};