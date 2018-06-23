import os
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class Spectrogram:
	xVals = None
	yVals = None
	fig = None
	ax = None
	def initFig():
		Spectrogram.fig, Spectrogram.ax = plt.subplots()

	def setVals(xVals, yVals):
		Spectrogram.xVals = xVals
		Spectrogram.yVals = yVals

	#Creates Spectrogram Line Plot
	def specPlot():
		Spectrogram.ax.plot(Spectrogram.xVals, Spectrogram.yVals, c='b', animated=True)
		Spectrogram.ax.set_title('Spectrogram')
		Spectrogram.ax.set_xlabel('Frequency (Hz)')
		Spectrogram.ax.set_ylabel('Intensity (dB)')
		#self.ax.set_ylim(top=70)

	#def dispPlot():
	#	plt.ion()
	#	plt.show()
	#	plt.pause(1)

#Spectrogram.initFig()
