param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CodexArgs
)

$documentsDir = Join-Path $HOME "Documents"
$codexFile = Join-Path $documentsDir "CODEX.md"

if (-not (Test-Path $codexFile)) {
    Write-Error "Missing workspace instructions: $codexFile"
    exit 1
}

$workspaceInstructions = Get-Content -Raw $codexFile
$bootstrapPrompt = @"
Read and follow the workspace instructions below before doing any work.

BEGIN WORKSPACE INSTRUCTIONS
$workspaceInstructions
END WORKSPACE INSTRUCTIONS
"@

& codex --cd $documentsDir @CodexArgs $bootstrapPrompt
exit $LASTEXITCODE
