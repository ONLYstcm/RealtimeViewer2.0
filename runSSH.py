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

connection1 = ssh("199.88.192.160", "<USERNAME>", "<PASSWORD>")
connection1.sendCommand("mkdir testfolder")
