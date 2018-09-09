import numpy as np
import sys
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import obj2clist as obj

# Name: Lai Wei
# Email: laiw12@bu.edu

####################################################
# modify the following 5 functions
# all functions assume homogeneous coordinates in 3D
####################################################
def project(d):
    """
    returns the projection matrix corresponding to having the viewpoint at (0,0,d)
    and the viewing plane at z=0 (the xy plane).
    """
    
    A = [[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,-1/d,1]]    ## use the matrix in lecture
  
    A = np.array(A)
    return A
    # your code here

def moveTo(start, end):
    """
    returns the matrix corresponding to moving an obj from position 'start' to position 'end.'
    positions are given in 3D homogeneous coordinates.
    """
    # your code here
    x = end[0] - start[0]
    y = end[1] - start[1]
    z = end[2] - start[2]
    A = [[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]]   ## the translation matrix from the book
    A = np.array(A)
    return A
    
def rotate(x,y,z,loc):
    """
    returns the matrix corresponding to first rotating a value 'x' around the x-axis,
    then rotating 'y' around the y-axis, and then 'z' around the z-axis.   All angles
    are in radians. The center of   rotation is at point given by 'loc' (3D homogeneous coord).
    """
    A = moveTo([0,0,0],loc)       ## the translation matrix that moves the origin to loc c.
    B = moveTo(loc,[0,0,0])       ## moves loc to orgin
    X1 = np.array([[1,0,0,0],[0,np.cos(x),-np.sin(x),0],[0,np.sin(x),np.cos(x),0],[0,0,0,1]]) ##rotation matrix
    Y1 = np.array([[np.cos(y),0,np.sin(y),0],[0,1,0,0],[-np.sin(y),0,np.cos(y),0],[0,0,0,1]]) ##rotation matrix
    Z1 = np.array([[np.cos(z),-np.sin(z),0,0],[np.sin(z),np.cos(z),0,0],[0,0,1,0],[0,0,0,1]]) ##rotation matrix
    U = np.dot(A,Z1)
    V = np.dot(U,Y1)
    W = np.dot(V,X1)
    return  np.dot(W,B)

def ballTransform(i,loc):
    """
    returns the appropriate transformation matrix for the ball.  The center of the ball
    before transformation is given by 'loc'.  The appropriate transformation depends on the
    timestep which is given by 'i'.
    """
    if i <=49:
        A = moveTo([0,0,0],[0,0,(i)*0.5])
        R = rotate(0,0,-i*0.5,loc)
        return np.dot(np.dot(project(100),R),A)
    if i >=50 and i <=64:
        A = moveTo([0,0,0],[0,0,49*0.5])
        B= moveTo([0,0,0],[-(i-50)*2,0,0])
        R= rotate((i-50)*2,0,0,loc)
        return np.dot(np.dot(np.dot(project(100),B) ,A),R)
    if i >=65 and i <= 149:
        A = moveTo([0,0,0],[0,0,50*0.5])      
        B = moveTo([0,0,0],[-(14)*2,0,0])
        F = np.dot(B,A)                                   ## final postion at time i = 64
          
        R=rotate(0,(-(2*np.pi/85)*(i-65)),0,[0,0,0])
        return np.dot(np.dot(project(100),R),F)

def houseTransform(i,loc):
    """
    returns the appropriate transformation matrix for the house.  The center of the house
    before transformation is given by 'loc'.  The appropriate transformation depends on the
    timestep which is given by 'i'.
    """

    
    if i<=64:
        return project(100)
    if i>=65 and i <=149:
        R=rotate(0,(-(2*np.pi/85)*(i-65)),0,[0,0,0]) ### rotate with orgin 
        return np.dot(project(100),R)
        

#######################################
# No need to change any code below here
#######################################
def scale(f):
    """
    returns a matrix that scales a point by a factor f
    """
    return(np.array([[f,0.,0,0],[0,f,0,0],[0,0,f,0],[0,0,0,1]]))

# This function implements the animation.  It will be called automatically if you
# run this entire file in the python interpreter.  Or you call call runShow() directly from the
# interpreter prompt if you wish.
def runShow():

    # read house data
    # house is 10*houseScale feet high
    with open('basicHouse.obj','r') as fp:
        house = obj.obj2flist(fp)
    house = obj.homogenize(house)
    houseScale = 3.0
    S = scale(houseScale)
    d = np.array([-5., 4., 3., 1]) - obj.objCenter(house) 
    M = np.array([[1.,0,0,d[0]],[0,1,0,d[1]],[0,0,1,d[2]],[0,0,0,1]])
    house = [S.dot(M).dot(f) for f in house]

    # read ball data
    # ball has radius equal to ballScale feet
    with open('snub_icosidodecahedron.wrl','r') as fp:
        ball = obj.wrl2flist(fp)
    ball = obj.homogenize(ball)
    ballScale = 2.0
    S = scale(ballScale)
    d = np.array([10.0, -0.5, 0., 1]) - obj.objCenter(ball)
    M = np.array([[1.,0,0,d[0]],[0,1,0,d[1]],[0,0,1,d[2]],[0,0,0,1]])
    ball = [S.dot(M).dot(f) for f in ball]

    # set up drawing region
    fig = plt.figure()
    ax = plt.axes(xlim=(-50,50),ylim=(-50,50))
    plt.plot(-40,-40,'')
    plt.plot(40,40,'')
    plt.axis('equal')

    # create drawables
    ballLines = []
    for b in ball:
        ballLines += ax.plot([],[],'b')
    houseLines = []
    for h in house:
        houseLines += ax.plot([],[],'r')

    # this is the drawing routine that will be called on each timestep
    def animate(i):
        M = ballTransform(i,obj.objCenter(ball))
        for b,l in zip(ballLines, ball):
            n = M.dot(l)
            b.set_data(n[0]/n[3],n[1]/n[3])
        M = houseTransform(i,obj.objCenter(house))
        for b,l in zip(houseLines, house):
            n = M.dot(l)
            b.set_data(n[0]/n[3],n[1]/n[3])
        fig.canvas.draw()
        return houseLines,ballLines
    
    # instantiate the animator.
    # we are animating at max rate of 25Hz
    # about the slowest that gives a sense of continuous motion
    # but this will slow down if the scene takes too long to draw
    anim = animation.FuncAnimation(fig, animate, 
                                    frames=150, interval=1000/25, repeat=False, blit=False)
    plt.show()
    
if __name__ == "__main__":
    runShow()


    
