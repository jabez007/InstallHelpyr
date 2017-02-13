Param( #Must be the first statement in your script
	[string]$SourceRoot,
	[string]$DestinationServer
	)

	Copy-Item -Path $SourceRoot\Release\Interconnect -Destination \\$DestinationServer\c$\Temp\Interconnect -recurse -force

    exit $LASTEXITCODE
