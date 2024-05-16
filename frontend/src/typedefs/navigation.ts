export interface Page {
    name: string;
    type: string;
    link?: string;
    elements?: Array<SubPage>;
    tooltip?: string;
}

export interface SubPage {
    name: string;
    link: string;
    tooltip: string;
}