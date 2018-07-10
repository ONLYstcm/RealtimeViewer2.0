############################################################
#This is the Spectrogram UI. Run this to run the entire app#
############################################################

#Do note that if a pol0.scio file already exists, the first graph may graph that data. However, as long as the experiment is running, that will change. 
#It will graph new data on the first graph if the data transport is successful. Not a source of worry. The program will continue collecting the latest data every 2 seconds.


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

runGraph.Spectrogram.initFig()

#fig, ax = plt.subplots()
#xdata, ydata = [], []
#ax.set_title('Spectrogram')
#ax.set_xlabel('Frequency (Hz)')
#ax.set_ylabel('Intensity (dB)')
#line, = plt.plot(xdata, ydata, 'k', animated=True)
newConnection = runSSH.ssh('10.0.0.1', 'pi', 'raspberry')
def init():
    #Creates folder for holding the python file in main directory
    #SSH
    try:
        os.mkdir(os.getcwd() + '/' + 'pol0scio')
    except:
        print("Folder exists")
    #runGraph.Spectrogram.initFig()

def timeSort(path): #Thanks to https://stackoverflow.com/questions/4500564/directory-listing-based-on-time
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))

def viewerUI(path): #Path should be the compressed pol0.scio.bz2
    #Decompress pol0.scio.bz2 file
    #global xdata, ydata

    if 'pol0.scio.bz2' in path:
        fScio = b2.decomp(path)
    else:
        fScio = path
    #try:
    #    fScio = b2.decomp(path) #Not needed unless it is compressed
    #except:
    #    fScio = path
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
    try:
        #PROF DOESNT WANT AVERAGE. WANTS LATEST
        scioArr = openScio.scioRead(fScio)

        #This returns the values we need for the x axis (frequencies)
        ratio = 250/scioArr[0].size
        freq = np.arange(scioArr[0].size)
        freq = ratio*freq

        #Takes log base 10 of the values
        scioArr = 10*np.log10(scioArr) - 147 #147 is the offset

        #Make first value 0 because this is the DC Voltage
        #for i in range(len(scioArr)):
        #   scioArr[i][0] = 0

        #This calculates the average of the intensities
        #Call averaged intensities newArr
        newArr = []
        #List comprehension takes average
        for i in range(len(scioArr[0])):
            newArr += [sum([scioArr[j][i] for j in range(len(scioArr))])/len(scioArr)]
	
	#Offset by 10
        #for i in range(len(scioArr[-1])):
        #        scioArr[-1][i] -= 
        #Generates new line plot
        runGraph.Spectrogram.ax.clear()
        runGraph.Spectrogram.ax.plot(freq[2:], scioArr[-1][2:], c='b')
        runGraph.Spectrogram.ax.set_title('Spectrogram')
        runGraph.Spectrogram.ax.set_xlabel('Frequency (Hz)')
        runGraph.Spectrogram.ax.set_ylabel('Intensity (dBm)')
        runGraph.Spectrogram.ax.set_ylim(top=-10, bottom=-90) #Limits
    except:
        pass
    #plt.draw()
    #plt.pause(1)

#update should do the thing that changes what happens in the viewerUI function. This should re-run by the FuncAnimation, so it should work with a global variable
def update(num):
    #In case using os.getcwd() while in ssh will yield different directory
    direc = os.getcwd() 
    try:
        #Opens shell
        #newConnection.openShell()
        #This copies the latest file over to your root directory
        #newConnection.sendCommand("cd " + str(newConnection.sendCommand("ls data_70MHz/" + str(newConnection.sendCommand("ls data_70MHz | tail -2 | head -1 |")) + " " + "| tail -1")) + " && " + "scp pol0.scio.bz2 " + os.getcwd() + '/' + 'pol0scio')
        
        #Issues: Using str on the stdout return doesn't do anything except give some huge message
        #newConnection.sendCommand('cd data_70MHz' + " && " + 'cd ' + str(newConnection.sendCommand("ls | tail -2 | head -1")) + " && " 'cd ' + str(newConnection.sendCommand('ls | tail -1')) + " && " + "scp pol0.scio " + direc + '/' + 'pol0scio') #Ask if os.getcwd() will work outside of the bash and in the local machine
        output1 = newConnection.sendCommand('cd data_70MHz ' + " && " + "ls | tail -2 | head -1")
        output1 = str(output1, 'utf8')[:-1]
        #newConnection = runSSH.ssh('10.0.0.1', 'pi', 'raspberry') 
        output2 = newConnection.sendCommand('cd data_70MHz/' + output1 + ' && ' + 'ls | tail -1')
        output2 = str(output2, 'utf8')[:-1]
        #print(output1, output2)
        #output3 = newConnection.sendCommand('ls data_70MHz/' + output1 + '/' + output2)# + ' && ') #+ 'scp pol0.scio wcen2@10.0.0.19:C:/users/wcen2' + ' && ' + 'ls | tail -1')
        remotepath = '/home/pi/data_70MHz/' + output1 + '/' + output2 + '/pol0.scio'
        print("Collecting data...")
        t = paramiko.Transport(('10.0.0.1', 22))
        t.connect(username='pi', password='raspberry')
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(remotepath, direc + '/' + 'pol0scio/' + 'pol0.scio')
        print("Collected!")
        #print(output1, output2)
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
    except:
        print("No new data, using latest data.")
    sFile = ''
    latest = os.getcwd() + '/' + 'pol0scio'
    if 'pol0.scio' in os.listdir(latest):
        sFile = 'pol0.scio'
    else:
        assert(False)
    scioPath = latest + '/' + sFile
    #print(scioPath)
    viewerUI(scioPath)


def staticRun(): #This is without the continuous animation so that you dont crash
    init()
    update()

#staticRun()

ani = FuncAnimation(runGraph.Spectrogram.fig, update, init_func = init, interval=2000, blit=False) #runs every 2000 milliseconds
plt.show()
#LEARN TO DECOMPRESS TAR.GZ AND .BZ2 FILES OR FIND SOME WAY TO GRAPH THOSE FILES. "MIGHT JUST BE BECAUSE JOSE COMPRESSED THEM. THEY ARE PROBABLY ALREADY IN SCIO FORMAT"
#USE SCP BECAUSE SOCKETS ONLY REQUEST REQUEST FILES BUT NOT CHECK IF ITS NEW

#THE 11 ROWS FOR EACH SPECTRUM IS CREATED EVERY 4 SECONDS
