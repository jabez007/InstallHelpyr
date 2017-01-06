Param (
    [string]$server,
    [string]$instance,
    [string]$CAHost = "vs-icx6-24.epic.com",
    [string]$CA = "CE Internal Intermediate CA"
    )

Function Clean-Temp {
    if (Test-Path "\\$server\c$\Temp\Internal.req") { Remove-Item "\\$server\c$\Temp\Internal.req" }
    if (Test-Path "$localRequest") { Remove-Item "$localRequest" }
    if (Test-Path "$localIssued") { Remove-Item "$localIssued" }
    if (Test-Path "\\$server\c$\Temp\Internal.cer") { Remove-Item "\\$server\c$\Temp\Internal.cer" }
    }

    $localRequest = "$([environment]::CurrentDirectory)\Internal.req"
    $localIssued = "$([environment]::CurrentDirectory)\Internal.cer"

    # Intro/Info
    Write-Host This tool will create a certificate signed by 
    write-host the internal certificate authority for the 
    write-host specified environment.
    write-host

    # Create the request on the remote server
    $remoteExitCode = $(Invoke-Command -ComputerName $server -ScriptBlock {
        Param (
            [string]$instance
            )

            # Make sure we are running as Admin
            If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")){   
                $arguments = "& '" + $myinvocation.mycommand.definition + "'"
                Start-Process powershell -Verb runAs -ArgumentList $arguments
                Break
                }

            # Setup the .inf file for CertReq
            if (!$instance) { $subjectname = read-host "Enter the name of the environment" }
            else { $subjectname = $instance }

            $infFile = @"
[NewRequest]
Subject = "CN=$subjectname,O=Internal"
;properties
KeyLength = 2048
KeyAlgorithm = RSA
Exportable = true
HashAlgorithm = sha256
KeyUsage = "CERT_DIGITAL_SIGNATURE_KEY_USAGE | CERT_KEY_ENCIPHERMENT_KEY_USAGE | CERT_DATA_ENCIPHERMENT_KEY_USAGE"

[EnhancedKeyUsageExtension]
OID=1.3.6.1.5.5.7.3.1
OID=1.3.6.1.5.5.7.3.2
"@

            Out-File -FilePath "C:\Temp\CreateInternalSigned.inf" -InputObject $infFile

            Write-Host "Creating new certificate request"
            Certreq -q -new -machine "C:\Temp\CreateInternalSigned.inf" "C:\Temp\Internal.req"
            if ($LASTEXITCODE -ne 0) {
                Write-Host "ERROR generating certificate"
                Return $LASTEXITCODE
                }
            Return 0
            } -ArgumentList $instance)
    if ($remoteExitCode[$remoteExitCode.Length-1] -ne 0) {
        Clean-Temp
        Exit $remoteExitCode
        }
    
    # Copy the request file back to local machine
    Copy-Item -Path \\$server\c$\Temp\Internal.req -Destination $localRequest

    # Submit request to CA from local machine
    Write-Host "Submiting certificate request to $CA"
    $request = Certreq -q -submit -config "$CAHost\$CA" $localRequest | Out-String
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR submitting request"
        Clean-Temp
        Exit $LASTEXITCODE
        }

    # Get RequestID
    $requestRegex = $request | Select-String 'RequestId: (\d+)'
    if ($requestRegex) {
        $requestID = $requestRegex.Matches[0].Groups[1].Value.Trim()
        }
    else {
        Write-Host "Request ID not found"
        Clean-Temp
        Exit -1
        }

    # Issue requested certificate
    $remoteExitCode = $(Invoke-Command -ComputerName $CAHost -ScriptBlock {
        Write-Host "Issuing Certificate" 
        certutil -resubmit $args[0]
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR issuing certificate"
            Return $LASTEXITCODE
            }
        Return 0 
        } -ArgumentList $requestID)
    if ($remoteExitCode[$remoteExitCode.Length-1] -ne 0) {
        Clean-Temp
        Exit $remoteExitCode
        }

    # Retrieve the issued certificate to the local machine
    Write-Host "Retrieving issued certificate from $CA"
    certreq -retrieve -config $CAHost\$CA $requestID $localIssued
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR retrieving certificate"
        Clean-Temp
        Exit $LASTEXITCODE
        }

    # Copy Issued Certificate back to remote server
    Copy-Item -Path $localIssued -Destination \\$server\c$\Temp\Internal.cer

    #Complete the Certificate request on the remote server
    $remoteExitCode = $(Invoke-Command -ComputerName $server -ScriptBlock {
        # Make sure we are running as Admin
        If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")){   
            $arguments = "& '" + $myinvocation.mycommand.definition + "'"
            Start-Process powershell -Verb runAs -ArgumentList $arguments
            Break
            }
       
        Write-Host "Completing certificate request"
        certreq -accept -machine C:\Temp\Internal.cer
        if ($LASTEXITCODE -ne 0) {
            Write-Host "ERROR completing request"
            Return $LASTEXITCODE
            }
        Return 0
        })
    if ($remoteExitCode[$remoteExitCode.Length-1] -ne 0) {
        Clean-Temp
        Exit $remoteExitCode
        }

    # Clean up
    Clean-Temp
    
    Write-Host "Certificate request for $instance completed"    
    #Read-Host "press enter to continue..."
    exit $LASTEXITCODE
