$SourceDir = ".\markdown_docs\images" # This denotes a 'source' folder in the current directory
$DestDir = ".\includes\figures" # This denotes a 'destination' folder in the current directory

# Create destination directory if it doesn't exist
if (-Not (Test-Path $DestDir)) {
    New-Item -ItemType Directory -Path $DestDir
}

# Iterate through .mmd files and process them
Get-ChildItem -Path $SourceDir -Filter *.mmd | ForEach-Object {
    $BaseName = $_.BaseName
    $OutputFile = Join-Path $DestDir "$BaseName.svg"
    mmdc -i $_.FullName -o $OutputFile -b weight 
}