import * as React from 'react';
import {useEffect} from 'react';
import {BarChart} from '@mui/x-charts/BarChart';
import {ProjectStatusDTO} from "../../typedefs/websocket_messages";
import i18next from "i18next";

const chartSetting = {
    xAxis: [
        {
            label: 'progress',
        },
    ],
    width: 500,
    height: 400,
};

const valueFormatter = (value: number) => `${value}%`;

type ChartData = {
    labels: string[];
    datasets: {
        data: number[];
        colors: ((opacity: number) => string)[];
    }[];
};

interface ProjectSendingProgressChartProps {
    data: ProjectStatusDTO;
}

export function ProjectSendingProgressChart(props: ProjectSendingProgressChartProps) {

    const {data} = props;

    const transformedData: ChartData = {
        labels: [],
        datasets: [{
            data: [],
            colors: []
        }]
    };

    data.runningTracks.forEach(track => {
        transformedData.labels.push(track.trackName);
        transformedData.datasets[0].data.push(track.progress);
        transformedData.datasets[0].colors.push(track.repeating ? (opacity => 'blue') : (opacity => '#112233'));
    });

    const dataset = data.runningTracks.map(track => ({
        trackName: track.dataSetName,
        progress: track.progress,
    }));

    useEffect(() => {
    }, [data]);
    return (
        dataset.length !== 0 ?
            <BarChart
                dataset={dataset}
                yAxis={[{scaleType: 'band', dataKey: 'trackName'}]}
                series={[{dataKey: 'progress', label: i18next.t("bar_chart_track_progress", {ns:['dialogs']}), valueFormatter}]}
                layout="horizontal"
                {...chartSetting}
            />
            : null
    );
}