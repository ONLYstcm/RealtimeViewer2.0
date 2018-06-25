from paramiko import client
#Base ssh class code implemented thanks to: https://daanlenaerts.com/blog/2016/01/02/python-and-ssh-sending-commands-over-ssh-using-paramiko/

class ssh:
	client = None

	def __init__(self, address, username, password):
		print("Connecting to server...")
		self.client = client.SSHClient()
		self.client.set_missing_host_key_policy(client.AutoAddPolicy())
		self.client.connect(address, username=username, password=password, look_for_keys=False)

	def sendCommand(self, command):
		if (self.client):
			stdin, stdout, stderr = self.client.exec_command(command)
			while not stdout.channel.exit_status_ready():
				if stdout.channel.recv_ready():
					alldata = stdout.channel.recv(1024)
					while stdout.channel.recv_ready():
						alldata += stdout.channel.recv(1024)

					print(str(alldata, "utf8"))
		else:
			print("Connection not opened.")
		print(stdout.read())
		output = stdout.read()
		return stdout

#connection1 = ssh("199.88.192.160", "<USERNAME>", "<PASSWORD>")
#connection1.sendCommand("mkdir testfolder")

'''
import threading, paramiko
 
class ssh:
    shell = None
    client = None
    transport = None
 
    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
 
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()
 
    def closeConnection(self):
        if(self.client != None):
            self.client.close()
            self.transport.close()
 
    def openShell(self):
        self.shell = self.client.invoke_shell()
 
    def sendShell(self, command):
        if(self.shell):
            self.shell.send(command + "\n")
        else:
            print("Shell not opened.")
 
    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                strdata = str(alldata, "utf8")
                strdata.replace('\r', '')
                print(strdata, end = "")
                if(strdata.endswith("$ ")):
                    print("\n$ ", end = "")
 
'''

 
''' 
connection = ssh(sshServer, sshUsername, sshPassword)
connection.openShell()
while True:
    command = input('$ ')
    if command.startswith(" "):
        command = command[1:]
    connection.sendShell(command)
'''