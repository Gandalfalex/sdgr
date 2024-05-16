import {SelectFormControl} from "../../../../../shared_components/SelectFormControl";
import {SelectChangeEvent} from "@mui/material/Select";
import {useEffect, useState} from "react";
import {ModelConfig} from "../../../../../../typedefs/django_types";
import {useTranslation} from "react-i18next";

interface SelectModelProps<T extends ModelConfig> {
    modelId: number;
    selectedConfig: T | null;
    setSelectedConfig: (model: T) => void;
    oldModelId?: number;
    fetchData: (id: number) => Promise<T[]>;
}


export function SelectConfigurationStep<T extends ModelConfig>(props: SelectModelProps<T>) {
    const {modelId, selectedConfig, setSelectedConfig, oldModelId, fetchData} = props;
    const [models, setModels] = useState<T[]>([]);
    const { t } = useTranslation(['headers']);

    const handleSolutionChange = (event: SelectChangeEvent<any>) => {
        const selectedSolutionId = event.target.value;
        const solution = models.find((s) => s.id === selectedSolutionId);
        setSelectedConfig(solution!);
    };

    useEffect(() => {
        fetchData(modelId).then(res => {
            setModels(res)
            if (oldModelId) {
                let tempData = res as T[]
                let oldSelection = tempData.filter(x => oldModelId === x.id)[0]
                setSelectedConfig(oldSelection);
            }
        });
        // @typescript-eslint/no-unused-vars
    }, [oldModelId]);
    return (
        <SelectFormControl
            label={t('select_configuration', {ns: ['headers']})}
            value={selectedConfig?.id}
            handleChange={handleSolutionChange}
            items={models}
            id="select-solution"
        />
    );
}
