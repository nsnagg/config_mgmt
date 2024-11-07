# This file: main_config_mgt.py
# The purpose of this file is to create a current configuration backup
# and compare it with the configuration backup from the previous day.
import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler
from device_inventory import DEVICE_INVENTORY
from rich import print as r_print
import sys


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


selection: str = ""
menu = ["1. Get Device Inventory", "2. Send Configuration", "3. Run Inventory List"]
print("\n" * 5)
print("************** Network Device Management ****************")
print("\n")
for selection in menu:
    print(selection)

choice = input("What do you want to do? 1, 2, or 3: ")

print(choice)

if choice == "1":
    print(menu[0])
elif choice == "2":
    print(menu[1])
    # compare_config_files()
elif choice == "3":
    print(menu[2])
    run_inventory_list(DEVICE_INVENTORY)
