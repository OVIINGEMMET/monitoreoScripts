# -*- coding: utf-8 -*-
import paramiko

source = r'/home/pc17/Desktop/getImage\rick/'
dest = '/var/www/html/panelview/img/sabancaya-test/'


print source.replace('\\', "/")

filename = 'sabancaya.jpg'

client = paramiko.SSHClient()
client.load_system_host_keys()
t = paramiko.Transport(('10.102.131.52', 22))
t.connect(username='root', password='rootubinas2016')
sftp = paramiko.SFTPClient.from_transport(t)

sftp.chdir(dest)
sftp.put(source + filename, filename)


sftp.close()
t.close()