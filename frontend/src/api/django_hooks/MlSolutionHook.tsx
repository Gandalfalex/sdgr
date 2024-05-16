import {useState} from "react";
import {MlConfig} from "../../typedefs/django_types";
import {patchSolutionSet, postNewSolutionSet, uploadTrainingFiles} from "../DjangoAPI";

export const useHandleSolutionAPI = () => {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<Error | undefined>();

    const handleSolutionAPI = async (
        isEdit: boolean,
        value: MlConfig,
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
                    data = await patchSolutionSet(value.ml_model, value.id, value.name, value.description, [...selectedItems, ...res], selectedTrainFiles);
                } else {
                    data = await postNewSolutionSet(value.ml_model, value.name, value.description, [...selectedItems, ...res], selectedTrainFiles);
                }
            } else {
                if (isEdit) {
                    data = await patchSolutionSet(value.ml_model, value.id, value.name, value.description, selectedItems, selectedTrainFiles);
                } else {
                    data = await postNewSolutionSet(value.ml_model, value.name, value.description, selectedItems, selectedTrainFiles);
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
        handleSolutionAPI,
        loading,
        error,
    };
};