param(
  [int]$Port = 8000,
  [switch]$OpenChrome
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$RuntimeDir = Join-Path $RepoRoot "runtime"
$OutLog = Join-Path $RuntimeDir "uvicorn-$Port.out.log"
$ErrLog = Join-Path $RuntimeDir "uvicorn-$Port.err.log"
$Url = "http://127.0.0.1:$Port"

New-Item -ItemType Directory -Force -Path $RuntimeDir | Out-Null

$listeners = netstat -ano | Select-String ":$Port\s+.*LISTENING"
foreach ($listener in $listeners) {
  $parts = ($listener.Line -split "\s+") | Where-Object { $_ -ne "" }
  $pidOnPort = [int]$parts[-1]
  if ($pidOnPort -gt 0) {
    Stop-Process -Id $pidOnPort -Force -ErrorAction SilentlyContinue
  }
}

$arguments = @(
  "-m", "uvicorn",
  "apps.api.main:app",
  "--host", "127.0.0.1",
  "--port", "$Port",
  "--app-dir", "$RepoRoot"
)

Start-Process `
  -FilePath "py" `
  -ArgumentList $arguments `
  -WorkingDirectory $RepoRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput $OutLog `
  -RedirectStandardError $ErrLog

$ready = $false
for ($i = 0; $i -lt 20; $i++) {
  Start-Sleep -Milliseconds 250
  try {
    $response = Invoke-RestMethod -Uri "$Url/health" -TimeoutSec 2
    if ($response.status -eq "ok") {
      $ready = $true
      break
    }
  } catch {
    # Keep polling until the server is ready or timeout is reached.
  }
}

if (-not $ready) {
  Write-Host "Oli API did not become ready. STDERR:"
  if (Test-Path $ErrLog) {
    Get-Content $ErrLog
  }
  exit 1
}

Write-Host "Oli API ready: $Url"
Write-Host "Docs: $Url/docs"

if ($OpenChrome) {
  Start-Process "chrome.exe" "$Url"
}

