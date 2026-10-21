# Registers the daily 12:00 KST DailyFeed run in Windows Task Scheduler (current user, only while logged on).
# Re-running replaces the existing task.  Usage:  pwsh -File scripts/register_task.ps1
$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root ".venv\Scripts\pythonw.exe"

$action = New-ScheduledTaskAction -Execute $Python -Argument "`"$Root\run.py`" auto" -WorkingDirectory $Root
$trigger = New-ScheduledTaskTrigger -Daily -At 12:00
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) -MultipleInstances IgnoreNew
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName "DailyFeed" -Description "DailyFeed: collect, summarize (opencode free LLM), publish to GitHub" `
    -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Get-ScheduledTask -TaskName "DailyFeed" | Get-ScheduledTaskInfo | Select-Object TaskName, NextRunTime
