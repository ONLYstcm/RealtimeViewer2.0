import openScio
import runGraph
import numpy as np 
import matplotlib.pyplot as plt

scioArr = openScio.scioRead('C:/Users/wcen2/RealtimeViewer2.0/pol0scio/pol0.scio')
ratio = 250/scioArr[0].size
freq = np.arange(scioArr[0].size)
freq = ratio*freq
scioArr = 10*np.log10(scioArr)
newArr = []
for i in range(len(scioArr[0])):
    newArr += [sum([scioArr[j][i] for j in range(len(scioArr))])/len(scioArr)]
print(freq, newArr)
runGraph.Spectrogram.initFig()
runGraph.Spectrogram.setVals(freq, newArr)
runGraph.Spectrogram.specPlot()
plt.show()