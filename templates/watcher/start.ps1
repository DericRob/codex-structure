param(
    [int]$Port = 9999,
    [switch]$OpenBrowser
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $scriptDir "watcher.pid"
$serverPath = Join-Path $scriptDir "server.py"
$pythonCmd = Get-Command python -ErrorAction Stop
$pythonExe = $pythonCmd.Source
$pythonwExe = Join-Path (Split-Path $pythonExe -Parent) "pythonw.exe"
$launcherExe = if (Test-Path $pythonwExe) { $pythonwExe } else { $pythonExe }
$watcherUrl = "http://127.0.0.1:$Port"
$healthUrl = "$watcherUrl/api/health"

if (Test-Path $pidFile) {
    $existingPid = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
    if ($existingPid) {
        $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
        if ($existingProcess) {
            try {
                Invoke-WebRequest -UseBasicParsing $healthUrl -TimeoutSec 2 | Out-Null
                Write-Output "Watcher already running (PID $existingPid)"
                Write-Output "Dashboard: $watcherUrl"
                exit 0
            } catch {
                Stop-Process -Id $existingPid -Force -ErrorAction SilentlyContinue
            }
        }
    }
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}

Write-Output "Starting Zero Trust Watcher..."
$process = Start-Process `
    -FilePath $launcherExe `
    -ArgumentList "-B", $serverPath, "--port", $Port `
    -WorkingDirectory $scriptDir `
    -WindowStyle Hidden `
    -PassThru

Set-Content -Path $pidFile -Value $process.Id

$ready = $false
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Milliseconds 250
    try {
        Invoke-WebRequest -UseBasicParsing $healthUrl -TimeoutSec 2 | Out-Null
        $ready = $true
        break
    } catch {
        if (-not (Get-Process -Id $process.Id -ErrorAction SilentlyContinue)) {
            break
        }
    }
}

if (-not $ready) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    if (Get-Process -Id $process.Id -ErrorAction SilentlyContinue) {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
    throw "Watcher failed to start or did not become healthy at $healthUrl"
}

Write-Output "Watcher running (PID $($process.Id))"
Write-Output "Dashboard: $watcherUrl"

if ($OpenBrowser) {
    Start-Process $watcherUrl | Out-Null
}
