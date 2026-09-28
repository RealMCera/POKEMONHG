param(
    [string]$WorkRoot = "$HOME\Downloads\PokemonFirstMovieHGSS",
    [string]$HeartGoldRom = "$HOME\Downloads\Pokemon - HeartGold Version (USA)(1).nds"
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

Write-Host ""
Write-Host "Ready at: $WorkRoot"
Write-Host "Branch: first-movie"
Write-Host "Verified local ROM copied to .first_movie\pokeheartgold.us.nds"
Write-Host "Do not commit the retail ROM."
