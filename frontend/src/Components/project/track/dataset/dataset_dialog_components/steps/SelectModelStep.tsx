import {SelectFormControl} from "../../../../../shared_components/SelectFormControl";
import {SelectChangeEvent} from "@mui/material/Select";
import {useEffect, useState} from "react";
import {Model} from "../../../../../../typedefs/django_types";
import {useTranslation} from "react-i18next";

interface SelectModelProps<T extends Model> {
    selectedModel: T | null;
    setSelectedModel: (model: T) => void;
    oldModelId?: number;
    fetchData: () => Promise<T[]>;
}

export function SelectModelStep<T extends Model>(props: SelectModelProps<T>) {
    const {setSelectedModel, selectedModel, oldModelId, fetchData} = props;
    const [models, setModels] = useState<T[]>([]);
    const { t } = useTranslation(['headers']);

    const handleModelChange = (event: SelectChangeEvent<any>) => {
        const selectedModelId = event.target.value;
        const model = models.find((m) => m.id === selectedModelId);
        setSelectedModel(model!);
        fetchData().then(res => setModels(res));
    };
    useEffect(() => {
        fetchData().then(res => {
            setModels(res);
            if (oldModelId) {
                const oldSelection = res.find(x => oldModelId === x.id);
                setSelectedModel(oldSelection!);
            }
        });
    }, [oldModelId, fetchData]);
    return (
        <SelectFormControl
            label={t('select_model', {ns: ['headers']})}
            value={selectedModel?.id}
            handleChange={handleModelChange}
            items={models}
            id="select-model"
        />
    );
}