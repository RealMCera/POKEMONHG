param(
    [string]$WorkRoot = "$HOME\Downloads\PokemonFirstMovieHGSS",
    [string]$HeartGoldRom = "$HOME\Downloads\Pokemon - HeartGold Version (USA)(1).nds",
    [string]$TitleTop = "$HOME\Downloads\pokemon_first_movie_ds_top_256x192(1).png",
    [string]$TitleBottom = "$HOME\Downloads\pokemon_first_movie_ds_bottom_256x192(1).png"
)

$ErrorActionPreference = "Stop"

$ExpectedSha1 = "4FCDED0E2713DC03929845DE631D0932EA2B5A37"
$ProjectRemote = "https://github.com/RealMCera/POKEMONHG.git"

Write-Host "=== First Movie HGSS bootstrap ==="

if (!(Test-Path $HeartGoldRom)) {
    throw "HeartGold ROM not found: $HeartGoldRom"
}

$actual = (Get-FileHash $HeartGoldRom -Algorithm SHA1).Hash.ToUpperInvariant()
Write-Host "HeartGold SHA1: $actual"

if ($actual -ne $ExpectedSha1) {
    throw "ROM hash does not match the pret HeartGold target."
}

if (Test-Path $WorkRoot) {
    throw "Work folder already exists: $WorkRoot"
}

git clone $ProjectRemote $WorkRoot
Set-Location $WorkRoot
git checkout first-movie

New-Item -ItemType Directory -Force -Path ".first_movie" | Out-Null
Copy-Item $HeartGoldRom ".first_movie\pokeheartgold.us.nds"

New-Item -ItemType Directory -Force -Path ".first_movie\title" | Out-Null
if (Test-Path $TitleTop) {
    Copy-Item $TitleTop ".first_movie\title\top.png"
    Write-Host "Staged exact top title PNG."
} else {
    Write-Warning "Top title PNG not found at: $TitleTop"
}
if (Test-Path $TitleBottom) {
    Copy-Item $TitleBottom ".first_movie\title\bottom.png"
    Write-Host "Staged exact bottom title PNG."
} else {
    Write-Warning "Bottom title PNG not found at: $TitleBottom"
}

Write-Host ""
Write-Host "Ready at: $WorkRoot"
Write-Host "Branch: first-movie"
Write-Host "Verified local ROM copied to .first_movie\pokeheartgold.us.nds"
Write-Host "Title source folder: .first_movie\title"
Write-Host "Do not commit the retail ROM or private title-source staging folder."
