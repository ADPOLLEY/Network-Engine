from flask.wrappers import Response
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import AuthenticationException
from netmiko import NetMikoTimeoutException


def show(devices, commands):
    response = dict()
    for device in devices:
        commandResponse = list()
        ip_address = device["hostname_id"]
        try:
            net_connect = ConnectHandler(**device)
        except (AuthenticationException):
            print('Authentication failure: ' + ip_address)
            response.update({device["host"]: ["Authentication Error"]})
            continue
        except (NetMikoTimeoutException):
            print('Timeout to device: ' + ip_address)
            response.update({device["host"]: ["Timeout Error"]})
            continue
        except (EOFError):
            print('End of file while attempting device ' + ip_address)
            response.update(
                {device["host"]: ["End of file Error"]})
            continue
        except (SSHException):
            print('SSH Issue. Are you sure SSH is enabled? ' + ip_address)
            response.update({device["host"]: ["SSH Protocol Error"]})
            continue
        except Exception as unknown_error:
            print('Some other error: ' + str(unknown_error))
            response.update({device["host"]: ["Unknown Error"]})
            continue

        print(net_connect.find_prompt())
        for command in commands:
            output = net_connect.send_command(command)
            print(f"Executing >> {command} >> on device >> ",
                  device['host'], "\n", "*" * 60)
            print(output)
            commandResponse.append(
                f"{command}\n----------------------------------------------------- \n"+str(output))
        response.update({device["host"]: commandResponse})
        net_connect.disconnect()

    return (response)