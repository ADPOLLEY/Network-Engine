from app import app
from genericpath import isfile
from posixpath import join
from netmiko import ConnectHandler
from paramiko.ssh_exception import SSHException
from netmiko import AuthenticationException
from netmiko import NetMikoTimeoutException
from time import localtime, strftime
from os import listdir, remove
from werkzeug.wrappers import response
from flask import send_file
from zipfile import ZipFile

# Backup the configuration for selected device

appRoot = app.root_path


def backup(devices):
    response = dict()
    for device in devices:
        coommandRespons = list()
        ip_address = device["hostname_id"]
        try:
            net_connect = ConnectHandler(**device)
        except (AuthenticationException):
            print('Authentication failure: ' + ip_address)
            response.update({device["hostname_id"]: "Authentication failure"})
            continue
        except (NetMikoTimeoutException):
            print('Timeout to device: ' + ip_address)
            response.update({device["hostname_id"]: "Timeout to device"})
            continue
        except (EOFError):
            print('End of file while attempting device ' + ip_address)
            response.update(
                {device["hostname_id"]: "End of file while attempting device"})
            continue
        except (SSHException):
            print('SSH Issue. Are you sure SSH is enabled? ' + ip_address)
            response.update({device["hostname_id"]: "SSH Protocol Error"})
            continue
        except Exception as unknown_error:
            print('Some other error: ' + str(unknown_error))
            response.update({device["hostname_id"]: "Unknown Error"})
            continue

        print(net_connect.find_prompt())
        print(f"Running configuration Backup on on device >> ",
              device['host'], "\n", "*" * 60)
        output = net_connect.send_command("show run")
        if output:
            current_time = strftime("%b_%Y_%X", localtime())
            with open(f"{appRoot}/data/backup_config/{ip_address}_{current_time}.txt", 'w') as src:
                src.writelines(output)
            print("Configuration sucessfully backued on ./data/backup_config")
            response.update({device["hostname_id"]: "Backup completed"})
        net_connect.disconnect()
    print(response)
    return (response)


# List all the backuped configuration exist on the dir
def list_cisco_backup():
    backup_file_list = list()
    backup_file_list = listdir(f"{appRoot}/data/backup_config/")
    return(backup_file_list)


# Delete the specific file form dir

def delete_cisco_backup(payload):
    response = str
    backup_file_name = payload[0]
    if isfile(f"{appRoot}/data/backup_config/{backup_file_name}"):
        delete_backup_file = remove(
            f"{appRoot}/data/backup_config/{backup_file_name}")
        response = "Backup file deleted"
    else:
        response = "File not exist" + str(backup_file_name)
    return(response)


def export_cisco_backup(payload):
    """Export the selected config files as Zip file"""
    appRoot = app.root_path
    sendZipFile = ZipFile(
        f"{appRoot}/data/Backup_config.zip", 'w')
    for configfile in payload["configfiles"]:
        fileName = f"{appRoot}/data/backup_config/{configfile}"
        sendZipFile.write(fileName, configfile)
    sendZipFile.close()
    sendZipFileName = f"{appRoot}/data/Backup_config.zip"
    return send_file(sendZipFileName, as_attachment=True)