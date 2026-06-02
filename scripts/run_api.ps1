param(
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

py -m uvicorn apps.api.main:app --host 127.0.0.1 --port $Port --app-dir $RepoRoot
