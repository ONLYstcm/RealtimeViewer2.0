############################################################
#This is the Spectrogram UI. Run this to run the entire app#
############################################################

import runSSH
import runGraph
import openScio
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import paramiko
import os
#import time, sched
import bz2Decompress as b2


def init():
	#Creates folder for holding the python file in main directory
	try:
		os.mkdir(os.getcwd() + '/' + 'pol0scio')
	except:
		pass
	runGraph.Spectrogram.initFig()

def timeSort(path): #Thanks to https://stackoverflow.com/questions/4500564/directory-listing-based-on-time
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def viewerUI(path): #Path should be the compressed pol0.scio.bz2
	#Decompress pol0.scio.bz2 file
	try:
		fScio = b2.decomp(path) #Not needed unless it is compressed
	except:
		fScio = path
	#Put this entire thing in a loop

	'''
	s = sched.scheduler(time.time, time.sleep)
	def do_something(sc): 
	    print "Doing stuff..."
	    # do your stuff
	    s.enter(60, 1, do_something, (sc,))

	s.enter(60, 1, do_something, (s,))
	s.run()
	'''

	#This converts the .scio file components to an array that we can graph
	scioArr = openScio.scioRead(fScio)

	#This returns the values we need for the x axis (frequencies)
	ratio = 250/scioArr[0].size
	freq = np.arange(scioArr[0].size)
	freq = ratio*freq

	#Takes log base 10 of the values
	scioArr = 10*np.log10(scioArr) 

	#Make first value 0 because this is the DC Voltage
	#for i in range(len(scioArr)):
	#	scioArr[i][0] = 0

	#This calculates the average of the intensities
	#Call averaged intensities newArr
	newArr = []
	#List comprehension takes average
	for i in range(len(scioArr[0])):
		newArr += [sum([scioArr[j][i] for j in range(len(scioArr))])/len(scioArr)]

	#Generates new line plot
	runGraph.Spectrogram.setVals(freq, newArr)
	runGraph.Spectrogram.specPlot()
	plt.show()
	#plt.draw()
	#plt.pause(1)

#update should do the thing that changes what happens in the viewerUI function. This should re-run by the FuncAnimation, so it should work with a global variable
def update():
	#In case using os.getcwd() while in ssh will yield different directory
	direc = os.getcwd()	
	#SSH
	newConnection = runSSH.ssh('10.0.0.1', 'pi', 'raspberry')
	#Opens shell
	#newConnection.openShell()
	#This copies the latest file over to your root directory
	#newConnection.sendCommand("cd " + str(newConnection.sendCommand("ls data_70MHz/" + str(newConnection.sendCommand("ls data_70MHz | tail -2 | head -1 |")) + " " + "| tail -1")) + " && " + "scp pol0.scio.bz2 " + os.getcwd() + '/' + 'pol0scio')
	
	#Issues: Using str on the stdout return doesn't do anything except give some huge message
	newConnection.sendCommand('cd data_70MHz' " && " 'cd ' + str(newConnection.sendCommand("ls | tail -2 | head -1")) + " && " 'cd ' + str(newConnection.sendCommand('ls | tail -1')) + " && " + "scp pol0.scio " + direc + '/' + 'pol0scio') #Ask if os.getcwd() will work outside of the bash and in the local machine
	#The above will not work because if it is completed, it will be in .scio.bz2 format.
	#This is where the scp occurs
	#This should re-run viewer function with different input
	#Diff input is determined by latest directory (the 15030) and the latest directory in that (150305414) and then pull out the scio file
	#use list dir and do [-1] to get latest by calling timeSort(path), where path is the original directory (so call it twice: once for initial number 15030, then one for the inside of that)
	
	###############################
	#####Gets Latest scio File#####
	###############################
	#gets some root path with all the numbered folders (call this var path)
	#Gives latest main folder
	'''
	bLatest = timeSort(path)[-1]
	#Gives latest sub folder
	sLatest = timeSort(path + '/' + bLatest)[-1]
	fPath = path + '/' + sLatest

	latest = os.listdir(fPath)
	for file in latest:
		if "pol0.scio" in file:
			sFile = file
	scioPath = fPath + '/' + sFile
	'''
	sFile = ''
	latest = os.getcwd() + '/' + 'pol0scio'
	for file in os.listdir(latest):
		if 'pol0.scio' in file:
			sFile = file
		else:
			assert(False)
	scioPath = latest + '/' + sFile
	#print(scioPath)
	viewerUI(scioPath)


def staticRun(): #This is without the continuous animation so that you dont crash
	init()
	update()

staticRun()

#ani = FuncAnimation(runGraph.Spectrogram.fig, viewerUI(), init_func = init, interval=500, blit=False)
#LEARN TO DECOMPRESS TAR.GZ AND .BZ2 FILES OR FIND SOME WAY TO GRAPH THOSE FILES. "MIGHT JUST BE BECAUSE JOSE COMPRESSED THEM. THEY ARE PROBABLY ALREADY IN SCIO FORMAT"
#USE SCP BECAUSE SOCKETS ONLY REQUEST REQUEST FILES BUT NOT CHECK IF ITS NEW

#THE 11 ROWS FOR EACH SPECTRUM IS CREATED EVERY 4 SECONDS