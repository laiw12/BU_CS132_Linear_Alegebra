import numpy as np

def innerProduct(a,b):
    """
    Takes two vectors a and b, of equal length, and returns their inner product
    """
    product = 0
    for i in range(len(a)):
        product = product + a[i]*b[i]
    return product

def AxIP(A,x):
    """
    Takes a matrix A and a vector x and returns their product
    """
    
    A = A.astype(float)
    m,n = np.shape(A) # m: row    n: column
    B=np.array([0]*m)
    B = B.astype(float)
    for i in range(0,m):
       B[i] = innerProduct(A[i,:],x)
       
       

    return B
    
   
        

def AxVS(A,x):
    """
    Takes a matrix A and a vector x and returns their product
    """
    A = A.astype(float)
    m,n = np.shape(A)
    B=np.array([0]*m)
    for i in range(0,n):
       B= B+ A[:,i]*x[i]
    return B
       
    
