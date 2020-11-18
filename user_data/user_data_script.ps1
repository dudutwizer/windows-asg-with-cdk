<powershell>
Import-Module AWSPowerShell
Install-WindowsFeature -name Web-Server -IncludeManagementTools
$instancetype = Invoke-RestMethod  http://169.254.169.254/latest/meta-data/instance-type
$instanceid= Invoke-RestMethod http://169.254.169.254/latest/meta-data/instance-id
$az= Invoke-RestMethod http://169.254.169.254/latest/meta-data/placement/availability-zone
$computername = $env:computername

Import-Module WebAdministration

$testparams = "<br><br>Hello from " + $computername + " instanceid: " + $instanceid + 
            "<br><br>I am running on " + $instancetype + " in availability zone " + $az
$testparams | Out-File 'C:\\inetpub\\wwwroot\\index.html'
</powershell>