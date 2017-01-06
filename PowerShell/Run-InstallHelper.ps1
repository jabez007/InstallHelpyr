Param( #Must be the first statement in your script
	[string]$Server,
	[string]$InstallRoot,
	[string]$InstallInstance
	)

    #### Interconnect InstallHelper ####
    # InstallHelper /[i|in|up|upr|u] [destinationPath] [instanceName(optional)] [appPoolName(optional)]
    # i = Install instance prefixed with Interconnect-
    # in = Install non-prefixed instance
    # up = Upgrade
    # upr = Upgrade and restart service
    # u = Uninstall
    # destinationPath = The path to the folder in which to install
    # instanceName = The name of the instance (optional)
    # appPoolName = The app pool to be used for this instance's virtual directory (optional)

	$remoteSession = new-pssession -computerName $Server
	
    Invoke-Command -Session $remoteSession -ScriptBlock {
        Param( #Must be the first statement in your script
	        [string]$InstallRoot,
	        [string]$InstallInstance
	        )
	    cmd /c C:\Temp\Interconnect\InstallHelper.exe /in "$InstallRoot\$InstallInstance" $InstallInstance
	    } -ArgumentList $InstallRoot,$InstallInstance
	
    $remotelastexitcode = invoke-command -Session $remotesession -ScriptBlock {$lastexitcode}

	exit $remotelastexitcode