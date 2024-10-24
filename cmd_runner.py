#!/user/bin/env python
from __future__ import absolute_import, division, print_function
import json
import my_tools
import netmiko
from netmiko.exceptions import NetmikoTimeoutException
from netmiko.exceptions import NetmikoAuthenticationException
from netmiko.exceptions import SSHException
import os
import sys
#import signal


# signal.signal(signal.SIGFPE, signal.SIG_DFL)   # IOError: Broken pipe
# signal.signal(signal.SIGINT, signal.SIG_DFL)    # KeyboardInterrupt: Ctrl-C

# if len(sys.argv) < 2:
#    print('Usage: cmd_runner.py commands.txt devices.json')

# username, password = my_tools.get_credentials()
username, password = 'admin', 'python'

with open('devices.json') as dev_file:
    devices = json.loads(dev_file.read())
    dev_file.read()

for device in devices:
    # Print seperator line
    print('~'*79)
    print(f"\n #### Connecting to the device {device['hostname']}  ####\n")

    # Remove/Add keys as required for connection
    del device['hostname']
    device['username'] = username
    device['password'] = password

    try:
        connection = netmiko.ConnectHandler(**device)
        enable = connection.enable()
    except NetmikoTimeoutException as e:
        print(f"Failed to {device['host']} {e}")
        continue
    except NetmikoAuthenticationException as e:
        print(f"{device['host']} {e}")
        continue
    except SSHException as e:
        print(f"{device['host']} {e}")
        continue

    print(connection.send_command('show run'))
    connection.disconnect()

