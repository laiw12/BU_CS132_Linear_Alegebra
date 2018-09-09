import numpy as np
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
    A = [[1,0,0,x],[0,1,0,y],[0,0,1,z],[0,0,0,1]]
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
        A = moveTo([0,0,0],[0,0,i*0.5])
        R = rotate(0,0,-i*0.5,loc)
        return np.dot(np.dot(project(100),A),R)
    if i >=50 and i <=64:
        A = moveTo([0,0,0],[0,0,49*0.5])
        B= moveTo([0,0,0],[-(i-50)*2,0,0])
        R= rotate((i-50)*2,0,0,loc)
        return np.dot(np.dot(np.dot(project(100),B) ,A),R) 

def houseTransform(i,loc):
  
        A = moveTo([0,0,0],[0,0,i*0.5])
        R = rotate(0,0,-i*0.5,loc)
        return project(100)
