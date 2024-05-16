import {TFunction} from "i18next";
import {cloneDeep} from "lodash";

export const translateSchema = (schema: any, t: TFunction) => {
    const translatedSchema = cloneDeep(schema);

    const translateRecursive = (obj: any) => {
        for (let key in obj){
            if(typeof(obj[key]) == "object")
                translateRecursive(obj[key]);
            else if(key === "description")
                obj[key] = t(obj[key]);
        }
    }
    translateRecursive(translatedSchema);
    return translatedSchema;
};