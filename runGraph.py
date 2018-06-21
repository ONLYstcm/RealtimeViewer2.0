import os
import matplotlib.pyplot as plt
import numpy as np

class Spectrogram:
	def __init__(self, xVals, yVals):
		self.xVals = xVals
		self.yVals = yVals
		self.fig, self.ax = plt.subplots()

	#Creates Spectrogram Line Plot
	def specPlot(self):
		self.ax.plot(self.xVals, self.yVals, c='b')
		self.ax.set_title('Spectrogram')
		self.ax.set_xlabel('Frequency (Hz)')
		self.ax.set_ylabel('Intensity (dB)')
		#self.ax.set_ylim(top=70)

	def dispPlot():
		plt.show()
