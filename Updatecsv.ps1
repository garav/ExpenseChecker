$dt = "1/1/2018"
$csvname = "expense.csv"
Write-host $MyInvocation.ScriptName
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$csvpath  = Join-Path -Path $scriptDir -ChildPath $csvname
echo $csvpath

Add-Type -Assembly "Microsoft.Office.Interop.Outlook"
$Outlook = New-Object -ComObject Outlook.Application
$Namespace = $Outlook.GetNameSpace("MAPI")
#$NameSpace.Folders.Item(1).Folders | FT FolderPath
$mails = $Namespace.Folders.Item(1).Folders.Item("Inbox").Folders.Item("CitiBank").Items| ?{$_.Subject -eq "Transaction confirmation on your Citibank credit card"}|?{[datetime]$_.CreationTIme -gt [datetime]$dt}|%{$_.body}

if (-Not (Test-Path($csvpath)))
{
    Set-Content -Value '"Amount","Merchant","Date","Balance","Description"' -Path $csvpath -Force
}
$Description = Import-csv $csvpath | %{$_.Description}

foreach( $m in $mails)
{

    $m -match '(\d+,{0,1}\d+\.\d+)[\s\S]*?(\d\d-\S\S\S-\d\d)\s+at\s(\S.*(?=The available))[\s\S]*?(\d*?,*?\d*?\.\d+)'
    $a = $Matches[1].Replace(",","")
    $b = $Matches[2]
    $c = $Matches[3].Replace(",","")
    $d = $Matches[4].Replace(",","")
    $e = $Matches[0].Replace(",","")
    
    if ($Description -match $e)
    {
        Write-host "present $e"
        continue
    }
    Write-host "not present $e"
    Add-Content -Value "$a,$c,$b,,,$e,$d" -Path $csvpath -Force
}
