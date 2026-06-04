# ─────────────────────────────────────────────────────────────────────────────
# run.ps1 – Levanta la aplicación en el ambiente indicado (Windows)
# Uso: powershell -ExecutionPolicy Bypass -File scripts\run.ps1 [-Env dev|test|prod]
# ─────────────────────────────────────────────────────────────────────────────
param(
    [ValidateSet("dev", "test", "prod")]
    [string]$Env = "dev"
)
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Task Manager – Iniciando ambiente: $Env" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Set-Location $Root

# ── Cargar variables del .env ─────────────────────────────────────────────────
$EnvFile = ".env.$Env"
if (Test-Path $EnvFile) {
    Write-Host " Cargando variables desde $EnvFile ..."
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]*)\s*=\s*(.*)\s*$') {
            $key   = $Matches[1].Trim()
            $value = $Matches[2].Trim()
            [Environment]::SetEnvironmentVariable($key, $value, "Process")
        }
    }
} else {
    Write-Warning " $EnvFile no encontrado. Usando valores por defecto."
}

# ── Crear directorio de datos ─────────────────────────────────────────────────
$dbPath = $env:DATABASE_PATH
if ($dbPath) {
    $dbDir = Split-Path -Parent $dbPath
    if ($dbDir -and -not (Test-Path $dbDir)) {
        New-Item -ItemType Directory -Path $dbDir -Force | Out-Null
    }
}

$appEnv  = if ($env:APP_ENV)       { $env:APP_ENV }       else { "development" }
$port    = if ($env:PORT)          { $env:PORT }           else { "5000" }
$debug   = if ($env:DEBUG)         { $env:DEBUG }          else { "true" }
$dbShow  = if ($env:DATABASE_PATH) { $env:DATABASE_PATH }  else { "taskmanager.db" }

Write-Host " Ambiente:   $appEnv"
Write-Host " Puerto:     $port"
Write-Host " Debug:      $debug"
Write-Host " Base datos: $dbShow"
Write-Host ""

& py run.py
exit $LASTEXITCODE
