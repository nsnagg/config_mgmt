from jumpssh import SSHSession
server_session = SSHSession('10.10.10.100', 'nsnagg', password = 'nsnagg').open()
switch_session = server_session.get_remote_session('10.10.10.3', 'admin', password = 'python')

print(switch_session.get_cmd_output('show ip int brief'))

server_session.close()
