param(
    [string]$BindHost = "127.0.0.1",
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
$watcherUrl = "http://$BindHost`:$Port"
$healthUrl = "$watcherUrl/api/health"
$browserHost = if ($BindHost -eq "0.0.0.0") { "127.0.0.1" } else { $BindHost }
$browserUrl = "http://$browserHost`:$Port"

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

function Write-PidMetadata {
    param(
        [string]$PidValue
    )

    @(
        "PID=$PidValue"
        "HOST=$BindHost"
        "PORT=$Port"
        "SERVER=$serverPath"
    ) | Set-Content -Path $pidFile
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

if (Test-Path $pidFile) {
    $meta = Read-PidMetadata
    $existingPid = $meta.PID
    $existingPort = if ($meta.PORT) { $meta.PORT } else { "$Port" }
    $existingServer = if ($meta.SERVER) { $meta.SERVER } else { $serverPath }

    if (Test-WatcherProcess -PidValue $existingPid -ExpectedServer $existingServer -ExpectedPort $existingPort) {
        if ($existingPort -eq "$Port") {
            try {
                Invoke-WebRequest -UseBasicParsing $healthUrl -TimeoutSec 2 | Out-Null
                Write-Output "Watcher already running (PID $existingPid)"
                Write-Output "Dashboard: $browserUrl"
                exit 0
            } catch {
                # Restart below if health probe fails.
            }
        }

        Stop-Process -Id $existingPid -Force -ErrorAction SilentlyContinue
    }

    Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
}

Write-Output "Starting Zero Trust Watcher..."
$process = Start-Process `
    -FilePath $launcherExe `
    -ArgumentList "-B", $serverPath, "--host", $BindHost, "--port", $Port `
    -WorkingDirectory $scriptDir `
    -WindowStyle Hidden `
    -PassThru

Write-PidMetadata -PidValue $process.Id

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
    if (Test-WatcherProcess -PidValue $process.Id -ExpectedServer $serverPath -ExpectedPort "$Port") {
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    }
    throw "Watcher failed to start or did not become healthy at $healthUrl"
}

Write-Output "Watcher running (PID $($process.Id))"
Write-Output "Dashboard: $browserUrl"

if ($OpenBrowser) {
    Start-Process $browserUrl | Out-Null
}
