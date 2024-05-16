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
    data: TrainDataPreviewDT;
    processed_data: TrainDataPreviewDT;
    flags?: Array<Boolean>;
}

const PreprocessPreviewGraph = (props: PreviewProps) => {

    const options = {
        responsive: false,
        maintainAspectRatio: true,
        aspectRatio: 4 / 3,
        plugins: {
            legend: {
                display: true // Enable legend
            },
            title: {
                display: false
            }
        },
        scales: {
            x: {
                type: 'linear' as const,
                ticks: {
                    display: true
                }
            }
        },
        elements: {
            point: {
                radius: 0
            }
        }
    };

    const labels = ["original", "processed"];
    const defaultValues = Array(10).fill(0);
    let valuesToUse = props.data ? props.data.values : defaultValues;
    const formattedData = valuesToUse.map((value, index) => ({x: index, y: value}));

    valuesToUse = props.processed_data ? props.processed_data.values : defaultValues;
    const formattedProcessedData = valuesToUse.map((value, index) => ({x: index, y: value}));


    const data = {
        labels,
        datasets: [
            {
                label: 'original',
                data: formattedData,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.01
            },
            {
                label: 'preprocessed',
                data: formattedProcessedData,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.01,
                segment: {
                    borderColor: (ctx: { p1DataIndex: any; }) => {
                        const index = ctx.p1DataIndex;
                        const isCurrentOrNextAltered = props.flags![index] || props.flags![index + 1];
                        return isCurrentOrNextAltered ? 'red' : undefined;
                    }
                }
            }
        ]
    };

    return (
        <Line options={options} data={data} height={300} width={400}/>
    );
}

export default PreprocessPreviewGraph;