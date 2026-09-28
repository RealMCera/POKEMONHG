param(
    [string]$Top = "$HOME\Downloads\pokemon_first_movie_ds_top_256x192(1).png",
    [string]$Bottom = "$HOME\Downloads\pokemon_first_movie_ds_bottom_256x192(1).png"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $Top)) {
    throw "Top title PNG not found: $Top"
}
if (!(Test-Path $Bottom)) {
    throw "Bottom title PNG not found: $Bottom"
}

$dest = ".first_movie\title"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

Copy-Item -LiteralPath $Top -Destination "$dest\top.png" -Force
Copy-Item -LiteralPath $Bottom -Destination "$dest\bottom.png" -Force

Write-Host "Staged exact title assets:"
Write-Host "  $dest\top.png"
Write-Host "  $dest\bottom.png"
Write-Host ""
Write-Host "Source PNGs are copied byte-for-byte and remain unmodified."
Write-Host "The build will create DS palette/tile intermediates from these local copies."
