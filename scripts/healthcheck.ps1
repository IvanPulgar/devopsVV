# ─────────────────────────────────────────────────────────────────────────────
# healthcheck.ps1 – Verifica que la aplicación esté respondiendo (Windows)
# Uso: powershell -ExecutionPolicy Bypass -File scripts\healthcheck.ps1 [host] [port] [retries]
# ─────────────────────────────────────────────────────────────────────────────
param(
    [string]$HostName   = "localhost",
    [int]   $Port       = 5000,
    [int]   $MaxRetries = 5
)

$WaitSeconds = 3
$Url = "http://${HostName}:${Port}/api/health"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Healthcheck: $Url" -ForegroundColor Cyan
Write-Host " Reintentos máximos: $MaxRetries" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

for ($i = 1; $i -le $MaxRetries; $i++) {
    Write-Host " Intento $i/$MaxRetries ..."
    try {
        $response = Invoke-RestMethod -Uri $Url -Method GET -TimeoutSec 5 -ErrorAction Stop
        $json     = $response | ConvertTo-Json -Compress
        Write-Host " Respuesta: $json"
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host " RESULTADO: Servicio disponible en $Url" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        exit 0
    } catch {
        if ($i -lt $MaxRetries) {
            Write-Host " Servicio no disponible, esperando ${WaitSeconds}s ..."
            Start-Sleep -Seconds $WaitSeconds
        }
    }
}

Write-Host "============================================================" -ForegroundColor Red
Write-Host " ERROR: Servicio no disponible después de $MaxRetries intentos" -ForegroundColor Red
Write-Host "============================================================" -ForegroundColor Red
exit 1
