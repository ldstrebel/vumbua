$base = ''D:\Code\vumbua''
$out  = Join-Path $base ''_notebooklm-export''
New-Item -ItemType Directory -Force $out | Out-Null

function Merge-Files($files, $outPath, $label) {
    $parts = [System.Collections.Generic.List[string]]::new()
    foreach ($f in $files) {
        $rel = $f.FullName.Replace($base + [IO.Path]::DirectorySeparatorChar, '''')
        $parts.Add('''')
        $parts.Add(''---'')
        $parts.Add(''## FILE: '' + $rel)
        $parts.Add(''---'')
        $parts.Add('''')
        $parts.Add((Get-Content $f.FullName -Raw -Encoding UTF8))
    }
    [IO.File]::WriteAllText($outPath, ($parts -join [Environment]::NewLine), [Text.Encoding]::UTF8)
    $kb = [math]::Round((Get-Item $outPath).Length / 1KB)
    Write-Host (''Written ['' + $label + '']: '' + $kb + '' KB'')
}

$src = Join-Path $base ''sessions\transcripts\Aggregated Sessions.md''
Copy-Item $src (Join-Path $out ''all-transcripts.md'')
$kb = [math]::Round((Get-Item $src).Length / 1KB)
Write-Host (''Copied [all-transcripts]: '' + $kb + '' KB'')

$worldFiles = Get-ChildItem (Join-Path $base ''world'') -Recurse -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $worldFiles (Join-Path $out ''all-world-lore.md'') ''world-lore''

$locFiles = Get-ChildItem (Join-Path $base ''locations'') -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $locFiles (Join-Path $out ''all-locations.md'') ''locations''

$npcFiles = Get-ChildItem (Join-Path $base ''characters\npcs'') -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $npcFiles (Join-Path $out ''all-npcs.md'') ''npcs''

$pcFiles = Get-ChildItem (Join-Path $base ''characters\player-characters'') -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $pcFiles (Join-Path $out ''all-player-characters.md'') ''player-characters''

$planFiles = Get-ChildItem (Join-Path $base ''sessions\planning'') -Recurse -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $planFiles (Join-Path $out ''all-planning.md'') ''planning''

$storyboardFiles = Get-ChildItem (Join-Path $base ''sessions\storyboards'') -Filter ''*.md'' | Where-Object { $_.Length -gt 100 }
Merge-Files $storyboardFiles (Join-Path $out ''all-storyboards.md'') ''storyboards''

$refFiles = @(
    (Get-Item (Join-Path $base ''glossary.md'')),
    (Get-Item (Join-Path $base ''timeline.md'')),
    (Get-Item (Join-Path $base ''knowledge-tracker.md''))
)
Merge-Files $refFiles (Join-Path $out ''reference.md'') ''reference''

$zipPath = Join-Path $base ''vumbua-notebooklm.zip''
if (Test-Path $zipPath) { Remove-Item $zipPath }
Compress-Archive -Path (Join-Path $out ''*'') -DestinationPath $zipPath
$zkb = [math]::Round((Get-Item $zipPath).Length / 1KB)
Write-Host ''''
Write-Host (''Done! ZIP: '' + $zipPath + '' ('' + $zkb + '' KB)'')
Get-ChildItem $out | ForEach-Object { Write-Host (''  '' + $_.Name + '' - '' + [math]::Round($_.Length/1KB) + '' KB'') }
