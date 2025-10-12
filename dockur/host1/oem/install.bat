echo RUNNING OEM INSTALLATION > C:\install.txt

echo Install only the Active Directory RSAT tools >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Add-WindowsCapability -Online -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0" ^
 >> C:\install.txt

echo Install GPO Tools >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Add-WindowsCapability -Online -Name Rsat.GroupPolicy.Management.Tools~~~~0.0.1.0" ^
 >> C:\install.txt

echo Install OpenSSH Server >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0" ^
 >> C:\install.txt

echo Start the SSH server >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Start-Service sshd" ^
 >> C:\install.txt

echo Start the SSH server at boot >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Set-Service -Name sshd -StartupType 'Automatic'" ^
 >> C:\install.txt

echo Allow SSH in the firewall >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "New-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -DisplayName 'OpenSSH Server (sshd)' -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22" ^
 >> C:\install.txt

echo Apply the firewall rule to all profiles >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
 "Set-NetFirewallRule -Name 'OpenSSH-Server-In-TCP' -Profile Domain,Private,Public" ^
 >> C:\install.txt

echo Set the default shell to PowerShell >> C:\install.txt
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"$shellParams = @{ Path = 'HKLM:\SOFTWARE\OpenSSH'; Name = 'DefaultShell'; Value = 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe'; PropertyType = 'String'; Force = $true}; New-ItemProperty @shellParams" ^
 >> C:\install.txt