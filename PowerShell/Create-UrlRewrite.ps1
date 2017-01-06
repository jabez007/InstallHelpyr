Param( #Must be the first statement in your script
	[string]$arrServer,
	[string]$interconnect, 
	[string]$instance
	) 


	$ruleName = "CE_$instance"
	$matchUrl = "$instance/wcf/epic.community.hie/*"
	$actionUrl = "https://$interconnect.epic.com/$instance/wcf/epic.community.hie/{R:1}"
	

	Invoke-Command -computerName $arrServer -ScriptBlock {
		Param(
			[string]$ruleName,
			[string]$matchUrl, 
			[string]$actionUrl
			)
        $psPath = 'MACHINE/WEBROOT/APPHOST'
        $filter = "/system.webserver/rewrite/globalRules"

        $rewriteRules = Get-Webconfiguration -PsPath $psPath -Filter $filter

		$myRule = $rewriteRules.collection | Where {$_.match.url -eq $matchUrl}

		if (-not $myRule) {
            Write-Host "Creating $ruleName for $matchUrl"

            $ruleValues = @{
                Name = $ruleName
                patternSyntax = 'Wildcard'
                stopProcessing = 'True'
                match = @{
                    url = "$matchUrl"
                    ignoreCase = 'True'
                    negate = 'False'
                    }
                conditions = @{
                    logicalGrouping = 'MatchAll'
                    trackAllCaptures = 'False'
                    }
                action = @{
                    type = 'Rewrite'
                    url = "$actionUrl"
                    appendQueryString = 'True'
                    }
                }
            Add-WebConfigurationProperty -PsPath $psPath -Filter $filter -name "." -Value $ruleValues
            
            $conditionsValues = @{
                input = '{HTTPS}'
                matchType = 'Pattern'
                pattern = 'on'
                ignoreCase = 'True'
                negate = 'False'
                }
            Add-WebConfigurationProperty -PSPath $psPath -Filter "$filter/rule[@Name='$ruleName']/conditions" -Name "." -Value $conditionsValues
        }
	
		else {
            $foundName = $myRule.Name
			Write-Host "URL rewrite rule for $matchUrl already exists in $foundName"
			}
		} -Args $ruleName,$matchUrl,$actionUrl

	# Read-Host -Prompt "Press Enter to exit"
	exit $LASTEXITCODE