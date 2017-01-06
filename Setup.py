import os

import PowerShell


def main(bokrug_root, code_base, install_server, install_folder, instance_name, reverse_proxy):
    bokrug_path = os.path.join(bokrug_root, code_base)

    print bokrug_path, install_server, install_folder, instance_name, reverse_proxy

    PowerShell.run_install_helper(source_path=bokrug_path,
                                  destination_server=install_server,
                                  install_root=install_folder,
                                  instance_name=instance_name)

    PowerShell.create_url_rewrite(arr_server=reverse_proxy,
                                  interconnect_server=install_server,
                                  instance_name=instance_name)

    PowerShell.create_certificate(interconnect_server=install_server,
                                  instance_name=instance_name)

    '''
    PowerShell.update_instance_list(interconnect=install_server,
                                    instance=instance_name,
                                    version=code_base)
    '''
    return

# # # #
