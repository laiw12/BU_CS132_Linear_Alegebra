import numpy as np


def cal(k):
    A=[[1,1],[1,0]]
    A=np.array(A)
    C=[[1,1],[1,0]]
    C=np.array(A)
    
    B=[1,1]
    B=np.array(B)

    X=np.linalg.matrix_power(A, k-1)
    return np.dot(X,B)

'''
    if k==1:
        return B
    for i in range(0,k-2):
        A=np.dot(A,C)
    return np.dot(A,B)
   ''' 
