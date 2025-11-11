param(
  [string]$IpsFile  = ".\ips.txt",
  [string]$Wordlist = ".\wordlist.txt",
  [string]$OutDir   = ".\results",
  [int]$Threads    = 40,
  [int]$TimeoutSec = 10
)

$mc = "200-299,301,302,401,403"
if (-not (Test-Path $IpsFile)) { Write-Error "IpsFile not found: $IpsFile"; exit 1 }
if (-not (Test-Path $Wordlist)) { Write-Error "Wordlist not found: $Wordlist"; exit 1 }
New-Item -Path $OutDir -ItemType Directory -Force | Out-Null

Get-Content $IpsFile | ForEach-Object {
  $line = $_.Trim()
  if ($line -eq "" -or $line.StartsWith('#')) { return }
  $base = if ($line -match '^https?://') { $line.TrimEnd('/') } else { "http://$($line.TrimEnd('/'))" }
  $hostKey = ([uri]$base).Host + (if ([uri]$base).Port -ne 80 -and ([uri]$base).Port -ne 443 {":$(([uri]$base).Port)"} else {""})
  $safe = ($hostKey -replace '[\\/:*?"<>| ]','_')
  $jsonOut = Join-Path $OutDir "$safe.json"
  $txtOut  = Join-Path $OutDir "$safe.txt"

  & ffuf -u "$base/FUZZ" -w (Resolve-Path $Wordlist).ProviderPath -mc $mc -t $Threads -timeout $TimeoutSec -o $jsonOut -of json

  if (Test-Path $jsonOut) {
    try {
      $j = Get-Content $jsonOut -Raw | ConvertFrom-Json
      foreach ($r in $j.results) {
        $input = if ($r.input -is [string]) { $r.input } else { $r.input.value }
        "$($base.TrimEnd('/'))/$($input.TrimStart('/'))`t$($r.status)`t$($r.length)" | Out-File -FilePath $txtOut -Append -Encoding utf8
      }
    } catch { }
  }
}
