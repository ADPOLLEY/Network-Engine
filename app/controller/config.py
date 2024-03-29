from flask.wrappers import Response
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import NetMikoTimeoutException


def config(devices, commands):
    response = dict()
    for device in devices:
        ip_address = device["hostname_id"]
        try:
            net_connect = ConnectHandler(**device)
        except (NetMikoTimeoutException):
            print('Timeout to device: ' + ip_address)
            response.update({device["host"]: ["Timeout Error."]})
            continue
        except (EOFError):
            print('End of file while attempting device ' + ip_address)
            response.update(
                {device["host"]: ["End of file Error."]})
            continue
        except (SSHException):
            print('SSH Issue. Are you sure SSH is enabled? ' + ip_address)
            response.update({device["host"]: ["SSH Protocol Error."]})
            continue
        except Exception as unknown_error:
            print('Some other error: ' + str(unknown_error))
            response.update({device["host"]: ["Unknown Error."]})
            continue  

        print(net_connect.find_prompt())
        output = net_connect.send_config_set(commands)
        if output:
            print(f"Executing >> {commands} >> on device >> ",
                device['host'], "\n", "*" * 60)
            print(output)
            response.update({device["host"]: [output]})
        net_connect.disconnect()

        return (response)