#import runSSH
import runGraph
import openScio
import numpy as np 
import matplotlib.pyplot as plt

#This is the Spectrogram UI. Run this to run the entire app#

#This converts the .scio file components to an array that we can graph
#scioArr = openScio.scioRead('D:/pol0.scio')
#scioArr = openScio.scioRead('C:/Users/William Cen/Desktop/PRIZM-RTSA-master/pol0.scio')
scioArr = openScio.scioRead('C:/Users/William Cen/Documents/Green Bank Stuff/data_70MHz/15294/1529450985/pol0.scio')

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
newGraph = runGraph.Spectrogram(freq, newArr)
newGraph.specPlot()
runGraph.Spectrogram.dispPlot()


#LEARN TO DECOMPRESS TAR.GZ AND .BZ2 FILES OR FIND SOME WAY TO GRAPH THOSE FILES. "MIGHT JUST BE BECAUSE JOSE COMPRESSED THEM. THEY ARE PROBABLY ALREADY IN SCIO FORMAT"
#USE SCP BECAUSE SOCKETS ONLY REQUEST REQUEST FILES BUT NOT CHECK IF ITS NEW

