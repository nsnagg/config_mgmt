import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler
from device_inventory import DEVICE_INVENTORY
from rich import print as r_print
import sys

print(len(sys.argv), sys.argv)
exit()


def run_inventory_list(device_inventory):
    for each_device in device_inventory:
        net_connect = ConnectHandler(
            device_type=each_device["device_type"],
            host=each_device["host"],
            username=each_device["username"],
            password=each_device["password"]
    )
    enable = net_connect.enable()
    output = net_connect.send_command(command_string="show run")
    print(output)
    print("\n")


def compare_config_files():
    """"Connect to Arista device in Priviliged mode"""
    for device in DEVICE_INVENTORY:
        output = ''
        # Defining the file from yesterday, fro comparison
        device_cfg_old = 'cfgfiles/' + device['host'] + '_' + (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        # Writing the command output to a file for today
        with open('cfgfiles/' + device['host'] + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
            device_cfg_new.write(output + '\n')

        # Extracting the differences between yesterday's and today's files in HTML format
        with open(device_cfg_old, 'r') as old_file, open('cfgfiles/' + device["host"] + '_'
                                                         + datetime.date.today().isoformat(), 'r') as new_file:
            difference = difflib.HtmlDiff().make_file(fromlines=old_file.readlines(),
                                                      tolines=new_file.readlines(),
                                                      fromdesc='Yesterday', todesc='Today')


selection: str = ""
choice = ["1. Get Device Inventory", "2. Send Configuration", "3. Run Inventory List"]
print("\n" * 20)
print("************** Network Device Management ****************")
print("\n")
for selection in choice:
    print(selection)


run_inventory_list(DEVICE_INVENTORY)







