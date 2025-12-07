Param()
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

Set-Location -LiteralPath 'C:\Users\Rajkumar\BillGeneratorUnified'

$exclude = @(
    '\\.git\\',
    '\\.zip_cache\\',
    '\\autonomous_test_output\\',
    '\\FINAL_TEST_OUTPUT\\',
    '\\macro_outputs\\',
    '\\notesheet_test_output\\',
    '\\OUTPUT_FILES\\',
    '\\OUTPUT_FIRST_20_ROWS\\',
    '\\test_output_complete\\',
    '\\VALIDATION_OUTPUT\\'
)

$files = Get-ChildItem -Recurse -File -Force | Where-Object {
    $p = $_.FullName
    foreach($ex in $exclude){ if($p -match $ex){ return $false } }
    # Skip Excel temporary lock files like "~$*.xlsm" to avoid access errors
    if ($_.Name -match '^~\$') { return $false }
    return $true
}

$hashes = foreach($f in $files){
    try {
        $h = Get-FileHash -Algorithm SHA256 -LiteralPath $f.FullName -ErrorAction Stop
        [PSCustomObject]@{ Path = $f.FullName; Hash = $h.Hash; Length = $f.Length }
    } catch {
        # ignore files we can't read (e.g., locked by another process)
    }
}

$groups = $hashes | Group-Object Hash | Where-Object { $_.Count -gt 1 }

foreach($g in $groups){
    Write-Output ("=== Duplicate Group: {0} (Count: {1})" -f $g.Name, $g.Count)
    $g.Group | Sort-Object Length, Path | ForEach-Object { $_.Path }
}