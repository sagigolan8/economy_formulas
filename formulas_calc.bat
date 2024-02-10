function Install-Python3115 {
    # Ask the user for permission to install Python 3.11.5
    $userConsent = Read-Host "Do you want to install Python 3.11.5? (Y/N)"

    # Check if the user agreed
    if ($userConsent -eq 'Y' -or $userConsent -eq 'y') {
        Write-Host "User agreed to install Python 3.11.5."
        # Correct URL for the Python 3.11.5 installer
        $installerUrl = "https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe"
        $installerPath = "$env:TEMP\python-3.11.5-installer.exe"
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
        Start-Process -FilePath $installerPath -Args "/quiet InstallAllUsers=1" -Wait
        Remove-Item -Path $installerPath
        Write-Host "Python 3.11.5 installation completed."
    } else {
        Write-Host "User declined to install Python 3.11.5. Exiting..."
    }
}


$desiredVersion = "Python 3.11.5"
$commands = @("py", "python", "py3", "python3")
$versionFound = $false
$successfulCommand = $null

foreach ($command in $commands) {
    $installedVersion = & $command --version 2>&1
    if ($? -eq $true -and $installedVersion -like "*$desiredVersion*") {
        $versionFound = $true
        $commandFound
        $successfulCommand = $command
        break
    }
}

if (-not $versionFound) {
    Write-Host "Python version 3.11.5 is NOT installed."
    Install-Python3115
} else {
    Write-Host "${successfulCommand}: Python version 3.11.5 is installed."
     & $successfulCommand -3.11 "menu.py" 
}
