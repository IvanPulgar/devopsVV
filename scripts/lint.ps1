# ─────────────────────────────────────────────────────────────────────────────
# lint.ps1 – Analiza calidad de código con flake8 (Windows)
# Uso: powershell -ExecutionPolicy Bypass -File scripts\lint.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
 Write-Host " Analizando calidad de codigo (flake8)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Set-Location $Root

# ── Verificar flake8 ──────────────────────────────────────────────────────────
$checkFlake8 = & py -m flake8 --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Error "ERROR: flake8 no instalado. Ejecuta primero scripts\install.ps1"
    exit 1
}
Write-Host " flake8: $checkFlake8"
Write-Host " Analizando app/ ..."

& py -m flake8 app/
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host " Sin errores de estilo detectados." -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host " RESULTADO: Código cumple estándares de calidad." -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
} else {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host " RESULTADO: Se encontraron errores de estilo (codigo: $exitCode)" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
}

exit $exitCode
