import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
a = np.random.random((5,5))
im=plt.imshow(a, interpolation='none')

# initialization function: plot the background of each frame
def init():
    im.set_data(np.random.random((5,5)))
    return [im]

# animation function.  This is called sequentially
def update(i):
    a=im.get_array()
    a=a*np.exp(-0.001*i)    # exponential decay of the values
    im.set_array(a)
    return [im]

if __name__ == '__main__':
    anim = FuncAnimation(
        fig, 
        update, 
        frames=np.linspace(0,128),
        init_func=init,
        blit=True,
        interval=1/60*1000 #60 fps
    )
    if len(sys.argv) > 1 and sys.argv[1] == 'save':
        anim.save('dist/line.gif', dpi=80, writer='imagemagick')
    else:
        # plt.show() will just loop the animation forever.
        plt.show()