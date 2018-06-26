
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = [1]
y = [1]

fig, ax = plt.subplots()
line, = ax.plot(x, y, color='k')

def update(num, line):
	global x, y
	x[0] += 0.05
	y[0] += 0.05
	line.set_data(x, y)
	#line.axes.axis([0, 10, 0, 1])
	return line,

ani = animation.FuncAnimation(fig, update, fargs=[line],
                              interval=1000, blit=True)
#ani.save('test.gif')
plt.show()

'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot(xdata, ydata, 'k*', animated=True)

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-1, 1)
    return ln,

def update(frame):
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init, blit=True)
plt.show()
'''