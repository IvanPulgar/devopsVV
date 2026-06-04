# ─────────────────────────────────────────────────────────────────────────────
# test.ps1 – Ejecuta la suite de pruebas en ambiente test aislado (Windows)
# Uso: powershell -ExecutionPolicy Bypass -File scripts\test.ps1 [pytest-args]
# ─────────────────────────────────────────────────────────────────────────────
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs = @()
)

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Task Manager – Ejecución de pruebas" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Set-Location $Root

# ── Configurar ambiente de test aislado ───────────────────────────────────────
$env:APP_ENV       = "test"
$env:DEBUG         = "false"
$timestamp         = Get-Date -Format "yyyyMMddHHmmss"
$env:DATABASE_PATH = "$env:TEMP\taskmanager_test_$timestamp.db"

Write-Host " APP_ENV:       $env:APP_ENV"
Write-Host " DATABASE_PATH: $env:DATABASE_PATH"
Write-Host ""

# ── Ejecutar pytest ───────────────────────────────────────────────────────────
try {
    if ($ExtraArgs.Count -gt 0) {
        & py -m pytest @ExtraArgs
    } else {
        & py -m pytest
    }
    $exitCode = $LASTEXITCODE
} finally {
    # ── Limpiar BD temporal ───────────────────────────────────────────────────
    if (Test-Path $env:DATABASE_PATH) {
        Remove-Item -ErrorAction SilentlyContinue $env:DATABASE_PATH
        Write-Host " Base de datos temporal eliminada."
    }
}

if ($exitCode -eq 0) {
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host " RESULTADO: Todas las pruebas pasaron correctamente." -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
} else {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host " RESULTADO: FALLARON pruebas (código de salida: $exitCode)" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}

exit $exitCode
