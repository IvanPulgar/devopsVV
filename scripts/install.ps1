# ─────────────────────────────────────────────────────────────────────────────
# install.ps1 – Instala todas las dependencias del proyecto (Windows)
# Uso: powershell -ExecutionPolicy Bypass -File scripts\install.ps1
# ─────────────────────────────────────────────────────────────────────────────
$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Task Manager – Instalación de dependencias" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Directorio raíz: $Root"

Set-Location $Root

# ── Verificar Python ──────────────────────────────────────────────────────────
$pythonCmd = $null
foreach ($cmd in @("py", "python3", "python")) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        $pythonCmd = $cmd
        break
    }
}
if (-not $pythonCmd) {
    Write-Error "ERROR: Python no encontrado. Instálalo antes de continuar."
    exit 1
}
$pyVersion = & $pythonCmd --version 2>&1
Write-Host " Python: $pyVersion"

# ── Crear entorno virtual si no existe ───────────────────────────────────────
if (-not (Test-Path ".venv")) {
    Write-Host " Creando entorno virtual .venv ..."
    & $pythonCmd -m venv .venv
} else {
    Write-Host " Entorno virtual .venv ya existe."
}

# ── Activar entorno virtual ───────────────────────────────────────────────────
$venvPython = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    $venvPython = $pythonCmd
}
Write-Host " Actualizando pip ..."
& $venvPython -m pip install --upgrade pip -q

# ── Instalar dependencias ─────────────────────────────────────────────────────
Write-Host " Instalando dependencias desde requirements.txt ..."
& $venvPython -m pip install -r requirements.txt

Write-Host ""
Write-Host " Dependencias instaladas correctamente." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
