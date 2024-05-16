$runs = "50", "100", "150", "200", "250", "300", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800"
$algos = "CGAN-keras", "CGAN-tsgm"
$repeatCount = 10

docker build -t test_runs:1.0 .
docker run -m 8g --cpus 2 -d --name test_statistics test_runs:1.0

for ($i=1; $i -le $repeatCount; $i++) {
    Write-Host "Repeat count: $i"
    foreach ($algo in $algos)
    {
        foreach ($run in $runs)
        {
            Write-Host "Running Docker command with run = $run and algo = $algo"
            docker exec -it test_statistics python main.py -i $run -a $algo
            $fileName = "C:\Users\Ferag\PycharmProjects\scientificProject\stats\stats_${algo}_${run}.txt"
            Start-Sleep -s 10
            docker stats --no-stream --format "{ 'container': '{{.Name}}', 'memory': '{{.MemUsage}}', 'cpu': '{{.CPUPerc}}' }" >> $fileName
            docker restart test_statistics
        }
    }
}