param(
    [string]$Profile = "test",
    [string]$QueryFile = "queries/smoke_test.sql",
    [string]$ConfigFile = "C:\codes\pv\particular\particular\segredos\syg\redshift-profile.local.json",
    [switch]$DryRun,
    [switch]$Diagnostic,
    [bool]$Ssl = $true,
    [string]$ApplicationName = "syg-redshift-runner"
)

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$runner = Join-Path $projectRoot "src\redshift_runner\run_query.py"

if (-not (Test-Path -LiteralPath $runner)) {
    throw "Executor Python nao encontrado: $runner"
}

$args = @(
    $runner,
    "--profile", $Profile,
    "--query-file", (Join-Path $projectRoot $QueryFile),
    "--config-file", $ConfigFile,
    "--application-name", $ApplicationName
)

if ($DryRun) {
    $args += "--dry-run"
}

if ($Diagnostic) {
    $args += "--diagnostic"
}

if ($Ssl) {
    $args += "--ssl"
} else {
    $args += "--no-ssl"
}

python @args
