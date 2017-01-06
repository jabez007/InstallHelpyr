import subprocess
import os

POWERSHELL_DIR = os.path.dirname(os.path.realpath(__file__))

# # # #
'''
Setup Functions
'''


def run_install_helper(source_path, destination_server, install_root, instance_name):
    copy_codebase(source_path, destination_server)
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\Run-InstallHelper.ps1',
                          '-Server', destination_server,
                          '-InstallRoot', install_root,
                          '-InstallInstance', instance_name],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def copy_codebase(source_root, destination_server):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\Copy-CodeBase.ps1',
                          '-SourceRoot', source_root,
                          '-DestinationServer', destination_server],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def create_url_rewrite(arr_server, interconnect_server, instance_name):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\Create-UrlRewrite.ps1',
                          '-arrServer', arr_server,
                          '-interconnect', interconnect_server,
                          '-instance', instance_name],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def create_certificate(interconnect_server, instance_name):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\Create-InternalCertificate.ps1',
                          '-server', interconnect_server,
                          '-instance', instance_name],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def configure_interconnect():
    return


def update_instance_list(interconnect, instance, version):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\UpdateInstanceList.ps1',
                          '-server', interconnect,
                          '-instance', instance,
                          '-version', version],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result

# # # #


def get_users(interconnect):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\GetUsers.ps1',
                          '-server', interconnect],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def get_services():
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\GetInterconnectServices.ps1',
                          '-serversFile', '.\CEservers.txt'],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def change_service_logon(interconnect, instance, user):
    p = subprocess.Popen([r'powershell.exe',
                          '-ExecutionPolicy', 'Unrestricted',
                          r'.\ChangeServiceLogon.ps1',
                          '-server', interconnect,
                          '-serviceName', 'Interconnect-'+instance,
                          '-userName', user],
                         cwd=POWERSHELL_DIR)
    result = p.wait()
    return result


def change_service_status(server, service, current_status):
    if u'Running' in current_status:
        p = subprocess.Popen([r'powershell.exe',
                              '-ExecutionPolicy', 'Unrestricted',
                              r'.\StopInterconnectService.ps1',
                              '-server', server,
                              '-instance', service],
                             cwd=POWERSHELL_DIR)
        result = p.wait()
        return result
    elif u'Stopped' in current_status:
        p = subprocess.Popen([r'powershell.exe',
                              '-ExecutionPolicy', 'Unrestricted',
                              r'.\StartInterconnectService.ps1',
                              '-server', server,
                              '-instance', service],
                             cwd=POWERSHELL_DIR)
        result = p.wait()
        return result


def open_trace_folder(server, instance):
    full_path = os.path.join(r'\\'+server,
                             r'Interconnect Trace Files',
                             '-'.join(instance.split('-')[1:]))
    subprocess.Popen('explorer "{0}"'.format(full_path))
