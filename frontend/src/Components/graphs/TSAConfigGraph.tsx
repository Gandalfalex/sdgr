import React, {useEffect} from 'react';
import {Line} from 'react-chartjs-2';
import {
    CategoryScale,
    Chart as ChartJS,
    Legend,
    LinearScale,
    LineElement,
    PointElement,
    Title,
    Tooltip,
} from 'chart.js';
import {IconButton, ListItemIcon} from "@mui/material";
import SaveIcon from '@mui/icons-material/Save';
import {TSDConfig, TSDConfigData} from "../../typedefs/django_types";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface ConfigProps {
    element: TSDConfig;
    configuration: TSDConfigData;
    offsets: { [key: string]: number };
    setActiveOffsets: (offsets: { [key: string]: number }) => void;
    send: (trainDataId: number) => void;
}

const TSAConfigGraph = (props: ConfigProps) => {
    const {configuration, send, offsets, setActiveOffsets} = props;
    const rangeSize = configuration ? configuration.values[0].data.length : 0;

    const options = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {legend: {display: true}, title: {display: false}},
        scales: {
            x: {type: 'linear' as const, ticks: {display: true}},
            y: {type: 'linear' as const, ticks: {display: true}}
        },
        elements: {point: {radius: 0}}
    };


    const sumMap: { [key: number]: number } = {};

    configuration.values?.forEach((configLevel, index) => {
        const valuesToUse = configLevel.data || Array(10).fill(0);
        const offset = offsets[configLevel.level.toString()] || 0;
        valuesToUse.forEach((value, index) => {
            const xValue = (index + offset) % rangeSize;
            if (!sumMap[xValue]) {
                sumMap[xValue] = 0;
            }
            sumMap[xValue] += value;
        });
    });

    // Convert the sumMap to the same data format used for the other datasets
    const sumData = Object.keys(sumMap).map((xValue) => ({
        x: Number(xValue),
        y: sumMap[Number(xValue)]
    }));


    const datasets = [
        ...configuration.values.map((configLevel, index) => {
            const defaultValues = Array(10).fill(0);
            const valuesToUse = configLevel.data || defaultValues;
            const offset = offsets[configLevel.level.toString()] || 0;
            let formattedData = valuesToUse.map((value, index) => ({x: (index + offset) % rangeSize, y: value}));
            formattedData.sort((a, b) => a.x - b.x);

            if (configuration.level_config && configuration.level_config[index]) {
                formattedData.map(point => {
                    // @ts-ignore
                    return {x: point.x + configuration.level_config![index], y: point.y};
                });
            }

            return {
                label: `Level ${configLevel.level}`,
                data: formattedData,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.01,
                fill: false
            };
        }),
        {
            label: 'Sum',
            data: sumData,
            borderColor: 'rgb(255, 99, 132)',
            tension: 0.01
        }
    ];


    const handleSliderChange = (label: string, newValue: number) => {
        //offsets[label] = newValue
        const newOffsets = {
            ...offsets,
            [label]: newValue,
        };
        setActiveOffsets(newOffsets);
    };

    useEffect(() => {
        const newOffsets = {...offsets};
        configuration.values.forEach((dataObj, index) => {
            if (!newOffsets.hasOwnProperty(dataObj.level.toString())) {
                if (configuration.level_config && configuration.level_config[index]) {
                    // @ts-ignore
                    newOffsets[dataObj.level.toString()] = configuration.level_config[index];
                }
            }
        });
        setActiveOffsets(newOffsets);
    }, [configuration]);


    return (
        <div>
            <ListItemIcon style={{display: 'flex', justifyContent: 'flex-end'}}>
                <IconButton className={'growButton'} onClick={() => send(configuration.id)}>
                    {<SaveIcon/>}
                </IconButton>
            </ListItemIcon>
            <Line options={options} data={{datasets}}/>
            {configuration.values.map((configLevel, index) => (
                <div key={index} style={{textAlign: 'center'}}>
                    <label>{`Level ${configLevel.level}`}</label>
                    <input
                        type="range"
                        min="0"
                        max={rangeSize.toString()}
                        value={offsets[configLevel.level.toString()] || 0}
                        onChange={(e) => handleSliderChange(configLevel.level.toString(), parseInt(e.target.value))}
                    />
                </div>
            ))}
        </div>
    );
}
export default TSAConfigGraph;