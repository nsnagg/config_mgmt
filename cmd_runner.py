#!/user/bin/env python
from __future__ import absolute_import, division, print_function
import json
import nos_tools
import netmiko
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
import os
import sys
import signal

# signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)   # Keyboardinterrupt: Ctrl-C

'''
if len(sys.argv) < 3:
    print('Usage: cmd_runner.py commands.txt devices.json')
    exit()

# These lines are used when the command file and the devices file will be entered at the cli prompt
with open(sys.argv[1]) as cmd_file:
    devices = json.loads(dev_file.read())
    dev_file.read()

with open(sys.argv[2]) as dev_file:
    devices = json.loads(dev_file.read())
    dev_file.read()
'''

# username, password = nos_tools.get_credentials()
username, password = 'admin', 'python'
results = {'Successful': [], "Failed": []}

# Open the command.txt file
with open('commands.txt') as cmd_file:
    commands = cmd_file.readlines()
print(commands)

# Open devices file
with open('devices.json') as dev_file:
    devices = json.loads(dev_file.read())
    dev_file.read()

for device in devices:
    # Print seperator line
    print('~'*79)

    # Remove/Add keys as required for connection
    del device['hostname']
    device['username'] = username
    device['password'] = password

    try:
        connection = netmiko.ConnectHandler(**device)
        enable = connection.enable()
    except NetmikoTimeoutException as e:
        print(f"Failed to {device['host']} {e}")
        results['Failed'].append(device['host'])
        continue
    except NetmikoAuthenticationException as e:
        print(f"{device['host']} {e}")
        results['Failed'].append(device['host'])
        continue
    except SSHException as e:
        print(f"{device['host']} {e}")
        results['Failed'].append(device['host'])
        continue
    for cmd in commands:
        print(f"\n #### Connecting to the device {connection.base_prompt}  ####\n")
        print(f'Output of cmd: {cmd}')
        print(connection.send_command(cmd))
        results['Successful'].append(device['host'])

    connection.disconnect()

print(f"Successfull devices list: {results['Successful']}")
print(f"Failed devices list: {results['Failed']}")

