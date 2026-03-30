$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pidFile = Join-Path $scriptDir "watcher.pid"
$serverPath = Join-Path $scriptDir "server.py"

function Read-PidMetadata {
    if (-not (Test-Path $pidFile)) {
        return $null
    }

    $meta = @{
        PID = ""
        HOST = ""
        PORT = ""
        SERVER = ""
    }

    $lines = Get-Content $pidFile -ErrorAction SilentlyContinue
    if ($lines.Count -eq 1 -and $lines[0].Trim() -match '^\d+$') {
        $meta.PID = $lines[0].Trim()
        return $meta
    }

    foreach ($line in $lines) {
        if ($line -match '^(PID|HOST|PORT|SERVER)=(.*)$') {
            $meta[$matches[1]] = $matches[2].Trim()
        }
    }

    return $meta
}

function Get-WatcherCommandLine {
    param(
        [string]$PidValue
    )

    if (-not $PidValue) {
        return $null
    }

    try {
        $proc = Get-CimInstance Win32_Process -Filter "ProcessId = $PidValue" -ErrorAction Stop
        return [string]$proc.CommandLine
    } catch {
        return $null
    }
}

function Test-WatcherProcess {
    param(
        [string]$PidValue,
        [string]$ExpectedServer,
        [string]$ExpectedPort
    )

    if (-not $PidValue) {
        return $false
    }

    $cmdLine = Get-WatcherCommandLine -PidValue $PidValue
    if (-not $cmdLine) {
        return $false
    }

    if ($cmdLine -notlike "*$ExpectedServer*") {
        return $false
    }

    if ($ExpectedPort -and $cmdLine -notlike "*--port $ExpectedPort*") {
        return $false
    }

    return $true
}

if (-not (Test-Path $pidFile)) {
    Write-Output "Watcher is not running (no PID file)"
    exit 0
}

$meta = Read-PidMetadata
$watcherPid = $meta.PID
$watcherPort = $meta.PORT
$watcherServer = if ($meta.SERVER) { $meta.SERVER } else { $serverPath }

if (-not $watcherPid) {
    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    Write-Output "Watcher PID file was empty"
    exit 0
}

if (Test-WatcherProcess -PidValue $watcherPid -ExpectedServer $watcherServer -ExpectedPort $watcherPort) {
    Stop-Process -Id $watcherPid -Force
    Write-Output "Watcher stopped (PID $watcherPid)"
} elseif (Get-Process -Id $watcherPid -ErrorAction SilentlyContinue) {
    Write-Output "Watcher PID file points to a different process; refusing to stop PID $watcherPid"
} else {
    Write-Output "Watcher was not running (stale PID $watcherPid)"
}

Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
