import os
from netmiko import ConnectHandler
from rich import print as r_print
from device_inventory import DEVICE_INVENTORY


def send_config_file(config_file):
    net_connect = ConnectHandler(**my_device)
    output_config = net_connect.send_config_from_file(config_file=config_file)


def get_device_info():
    """Get important information from network device"""
    net_connect = ConnectHandler()
    output_show_version_text_fsm = net_connect.send_command(command_string="show version", use_textfsm=True)
    r_print(output_show_version_text_fsm)


def run_inventory_list(device_inventory):
    for each_device in device_inventory:
        net_connect = ConnectHandler(
            device_type=each_device["device_type"],
            host=each_device["host"],
            username=each_device["username"],
            password=each_device["password"]
        )
        output = net_connect.send_command(command_string="sh ip int bri")
        print(output)
        print("\n")


my_device = {
    "device_type": "arista_eos",
    "host": "10.10.10.2",
    "username": "admin",
    "password": "python",
    "port": "22"
}


choice = ["1. Get Device Inventory", "2. Send Configuration", "3. Run Inventory List"]
print("\n" * 20)
print("************** Network Device Management ****************")
print("\n")
for selection in choice:
    r_print(selection)
print("What would you like to do? Inpt number: ")
print("\n")
print(os.getcwd())

