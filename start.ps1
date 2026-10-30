# =====================================================================
#  Professor's Vet & Pet Care - Local Dev Server Launcher
#  Usage:  .\start.ps1            (auto-picks a free port)
#          .\start.ps1 -Port 8010 (force a specific port)
#  Checks: python installed -> deps installed -> port free -> migrations
#          -> static dir exists -> starts Django dev server.
# =====================================================================
param(
    [int]$Port = 0,
    [switch]$NoReload
)

$ErrorActionPreference = 'Stop'
$root = $PSScriptRoot
Set-Location $root

function Fail($msg) {
    Write-Host ""
    Write-Host "  [ERROR] $msg" -ForegroundColor Red
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "  Professor's Vet & Pet Care - starting local server..." -ForegroundColor Cyan

# 1) Python available?
$python = "python"
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    Fail "Python is not installed or not in PATH. Install Python 3.10+ and tick 'Add to PATH'."
}
Write-Host ("  Python: " + (& $python --version 2>&1))

# 2) Django + requirements installed? (auto-install if missing)
$depsOk = $true
try { & $python -c "import django, dotenv, whitenoise, dj_database_url" 2>$null; if ($LASTEXITCODE -ne 0) { $depsOk = $false } } catch { $depsOk = $false }
if (-not $depsOk) {
    Write-Host "  Installing dependencies from requirements.txt ..." -ForegroundColor Yellow
    & $python -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) { Fail "Dependency installation failed. Run: python -m pip install -r requirements.txt" }
}

# 3) Find a free port (never clash with other apps already using 8000)
function Test-PortFree([int]$p) {
    # Active listener => busy
    $conn = Get-NetTCPConnection -LocalPort $p -State Listen -ErrorAction SilentlyContinue
    if ($conn) { return $false }
    # Reserved by another process (e.g. Hyper-V / excluded port ranges) => busy
    $ip = $null
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $p)
        $listener.Start()
        $listener.Stop()
        return $true
    } catch { return $false }
}

if ($Port -eq 0) {
    $Port = 0
    foreach ($candidate in 8000..8010) {
        if (Test-PortFree $candidate) { $Port = $candidate; break }
    }
    if ($Port -eq 0) { Fail "No free port found between 8000 and 8010." }
} elseif (-not (Test-PortFree $Port)) {
    Fail "Port $Port is already in use by another program. Try: .\start.ps1 -Port 8011"
}

# 4) Keep ALLOWED_HOSTS / CSRF origins working for whatever port we picked
$env:DEBUG = "True"
$env:DJANGO_PORT = "$Port"

# 5) Ensure static dir exists (STATICFILES_DIRS must exist or Django warns)
if (-not (Test-Path (Join-Path $root 'static'))) { New-Item -ItemType Directory -Path (Join-Path $root 'static') -Force | Out-Null }

# 6) System check (catches misconfiguration before the browser shows an error page)
& $python manage.py check
if ($LASTEXITCODE -ne 0) { Fail "Django system check failed. Fix the errors shown above." }

# 7) Apply migrations automatically (safe: only pending ones run)
& $python manage.py migrate --noinput
if ($LASTEXITCODE -ne 0) { Fail "Database migration failed." }

Write-Host ""
Write-Host ("  Local site  ->  http://127.0.0.1:$Port/") -ForegroundColor Green
Write-Host ("  Admin panel ->  http://127.0.0.1:$Port/admin/   (admin / admin)") -ForegroundColor Green
Write-Host "  Press CTRL+C to stop." -ForegroundColor DarkGray
Write-Host ""

$args = @("manage.py", "runserver", "127.0.0.1:$Port")
if ($NoReload) { $args += "--noreload" }

& $python @args
