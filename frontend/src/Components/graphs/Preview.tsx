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
import {Line} from 'react-chartjs-2';
import {PreviewData} from '../../typedefs/spring_types';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface PreviewProps {
    data: PreviewData
}

const Preview = (props: PreviewProps) => {

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            title: {
                display: false
            }
        },
        scales: {
            x: {
                type: 'linear' as const,
                ticks: {
                    display: false
                }
            }
        },
        elements: {
            point: {
                radius: 0
            }
        }
    };

    const labels = props.data.labels;

    const data = {
        labels,
        datasets: [
            {
                label: 'Dataset',
                data: props.data.values,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.01
            }
        ]
    };

    return <Line options={options} data={data}/>;
}

export default Preview;
