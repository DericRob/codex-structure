$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $scriptDir "watcher.pid"

if (-not (Test-Path $pidFile)) {
    Write-Output "Watcher is not running (no PID file)"
    exit 0
}

$watcherPid = (Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1).Trim()
if (-not $watcherPid) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Output "Watcher PID file was empty"
    exit 0
}

$process = Get-Process -Id $watcherPid -ErrorAction SilentlyContinue
if ($process) {
    Stop-Process -Id $watcherPid -Force
    Write-Output "Watcher stopped (PID $watcherPid)"
} else {
    Write-Output "Watcher was not running (stale PID $watcherPid)"
}

Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
