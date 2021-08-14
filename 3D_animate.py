
import random
from itertools import count
from matplotlib import markers
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#plt.style.use('fivethirtyeight')

ax = plt.axes(projection='3d')

namafile = 'data3D.csv'
header1 = "x"
header2 = "y"
header3 = "z"

index = count()


def animate(i):
    data = pd.read_csv('data3D.csv')
    x = data[header1].to_numpy()[-5:-1]
    y = data[header2].to_numpy()[-5:-1]
    z = data[header3].to_numpy()[-5:-1]

    #print(type(x))
    plt.cla()

    ax.plot3D(x, y, z, 'black')
    ax.scatter(x[0], y[0], z[0], 'blue',marker='o')
    ax.scatter(x[1], y[1], z[1], 'red',marker='o')
    ax.scatter(x[2], y[2], z[2], 'green',marker='o')
    ax.scatter(x[3], y[3], z[3], 'yellow',marker='o')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim3d(-100, 100)
    ax.set_ylim3d(-200, 200)
    ax.set_zlim3d(-100, 100)


    #plt.legend(loc='upper left')
    #plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=500)


plt.tight_layout()
plt.show()
