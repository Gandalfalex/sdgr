import {Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, TimeScale, Title, Tooltip,} from 'chart.js';
import {Box,} from "@mui/material";
import {Line} from 'react-chartjs-2';
import {LogDataGraph} from '../../typedefs/spring_types';
import 'chartjs-adapter-date-fns';

ChartJS.register(
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface LogDataProps {
    data: LogDataGraph | undefined
}


const LogGraphElement = (props: LogDataProps) => {
    if (props == null) {
        return <Box/>
    }
    const options = {
        type: 'line',
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: true
            }
        },
        scales: {

            x: {
                type: 'time',
                time: {
                    unit: "second",
                },
                title: {
                    display: true,
                    text: 'time'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'send value'
                },
            }
        },
        elements: {
            point: {
                radius: 3
            }
        },
        outerWidth: 0.9,
    };

    if (props.data != null) {

        const data = {
            labels: props.data.labels,
            datasets: [
                {
                    data: props.data.values,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
        };

        // @ts-ignore
        return <Line options={options} data={data} height={300}/>
    }

    return <Box/>;
}

export default LogGraphElement;