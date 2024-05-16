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
import {TrainDataPreviewDT} from "../../typedefs/django_types";


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
    data: TrainDataPreviewDT,
    key: number
}

export const OneDisplayOnlyElementsGraph = (props: PreviewProps) => {

    const options = {
        responsive: true,
        maintainAspectRatio: true,
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
                },
                title: {
                    display: true,
                    text: props.data.name
                }
            }
        },
        elements: {
            point: {
                radius: 0
            }
        }
    };
    const labels: number[] = [];
    console.log( props.data.values.length)
    for (let i = 1; i <= props.data.values.length; i++) {
        labels.push(i);
    }

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
