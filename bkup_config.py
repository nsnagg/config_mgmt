# file: bkup_config.py
# This script will take a device configuration snapshot and put it in a file.
# This script will also create a diff file and send it to a configured email address.
import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler
from device_inventory import DEVICE_INVENTORY
import my_tools


def run_inventory_list(device_inventory):
    for each_device in device_inventory:
        net_connect = ConnectHandler(
            device_type=each_device["device_type"],
            host=each_device["host"],
            username=username,
            password=password,
            global_delay_factor=3
        )
        enable = net_connect.enable()
        output = net_connect.send_command(command_string="show run")
        # print(output)

        # Defining the file from yesterday, for comparison
        device_cfg_old = 'cfgfiles/' + each_device["host"] + '_' + (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

        # Writing the command output to a file for today
        with open('cfgfiles/' + each_device["host"] + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
            device_cfg_new.write(output + '\n')

        # Extracting html formated differences between yesterday's and today's configuration file
        with (open(device_cfg_old, 'r') as old_file,
              open('cfgfiles/' + each_device["host"] + '_' + datetime.date.today().isoformat(), 'r') as new_file):
            difference = difflib.HtmlDiff().make_file(fromlines=old_file.readlines(),
                                                      tolines=new_file.readlines(), fromdesc="Yesterday", todesc="Today")

        # Sending the differences via email
        # Defining the e-mail parameters
        fromaddr = 'nosnagg.dev@gmail.com'
        toaddr = 'nosnagg.dev@gmail.com'

        # More on MIME and multipart:
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Daily Configuration Management Report for " + str(datetime.date.today())
        msg.attach(MIMEText(difference, 'html'))

        # Sending the email via Gmail's SMTP server on port 587
        server = smtplib.SMTP('smtp.gmail.com', 587)

        # SMTP connection is in TLS (Transport Layer Security) mode. All SMTP commands that follow will be encrypted
        server.starttls()

        # Logging in to Gmail and sending the email
        server.login('nosnagg.dev@gmail.com', 'jnue smjz ydaf qocw')
        server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()


# Defining the command to send to each device
command = 'show running'

# Input username and passwords
username, password = my_tools.get_credentials()

# Get Device Inventory list
run_inventory_list(DEVICE_INVENTORY)

print("\n" * 2)
print("******************************************************************************")
print("*** Successfully!!! saved the current configuration file for each device.  ***")
print("*** And sent the diff file via email for each device.                      ***")
print("******************************************************************************")
# End Of Program
