#import runSSH
import runGraph
import openScio
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#import time, sched
#import bz2Decompress


def init():
	runGraph.Spectrogram.initFig()

def timeSort(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def viewerUI(path):
	#plt.ion()
	#This is the Spectrogram UI. Run this to run the entire app#

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
	#scioArr = openScio.scioRead('D:/pol0.scio')
	#scioArr = openScio.scioRead('C:/Users/William Cen/Desktop/PRIZM-RTSA-master/pol0.scio')
	#scioArr = openScio.scioRead('C:/Users/William Cen/Documents/Green Bank Stuff/data_70MHz/15294/1529450985/pol0.scio')
	#scioArr = openScio.scioRead('C:/Users/William Cen/Documents/pol0.scio')
	scioArr = openScio.scioRead(path)

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

	#plt.draw()
	#plt.pause(1)

#update should do the thing that changes what happens in the viewerUI function. This should re-run by the FuncAnimation, so it should work with a global variable
def update():	
	#This is where the scp occurs
	#This should re-run viewer function with different input
	#Diff input is determined by latest directory (the 15030) and the latest directory in that (150305414) and then pull out the scio file
	#use list dir and do [-1] to get latest by calling timeSort(path), where path is the original directory (so call it twice: once for initial number 15030, then one for the inside of that)
	
	pass

ani = FuncAnimation(runGraph.Spectrogram.fig, viewerUI(), init_func = init, interval=500, blit=False)
#LEARN TO DECOMPRESS TAR.GZ AND .BZ2 FILES OR FIND SOME WAY TO GRAPH THOSE FILES. "MIGHT JUST BE BECAUSE JOSE COMPRESSED THEM. THEY ARE PROBABLY ALREADY IN SCIO FORMAT"
#USE SCP BECAUSE SOCKETS ONLY REQUEST REQUEST FILES BUT NOT CHECK IF ITS NEW

C:/Users/William Cen/Documents/Green Bank Stuff/data_70MHz/15294