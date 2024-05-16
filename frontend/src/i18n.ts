import i18next from "i18next";
import {initReactI18next} from "react-i18next";
import detector from "i18next-browser-languagedetector";


const languages = ['en', 'de', 'ua', 'ru'];

const namespaces = ['main_page', 'dialogs', 'headers', 'components', 'schemas', 'survey', 'main_menu'];

const resources = {};

languages.forEach((language) => {
    // @ts-ignore
    resources[language] = {};

    namespaces.forEach((namespace) => {
        // @ts-ignore
        resources[language][namespace] = require(`./translations/${language}/${namespace}.json`);
    });
});


i18next
    .use(detector)
    .use(initReactI18next)
    .init({
        fallbackLng: "en",
        resources
    });

export default i18next;