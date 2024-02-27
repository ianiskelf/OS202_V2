from mpi4py import MPI
import numpy as np
from time import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


# Dimension du problème (peut-être changé)
dim = 120
# Initialisation de la matrice
A = np.array([[(i+j) % dim+1. for i in range(dim)] for j in range(dim)])

# Initialisation du vecteur u
u = np.array([i+1. for i in range(dim)])



def produit_classique(A,u):
    deb = time()
    res = A.dot(u)
    fin = time()
    print(f"Le temps classique est {fin-deb}")
    return res

def produit_colonne(A,u):
    
    deb = time()
    nb_col=dim//size 
    
    start=rank*nb_col
    end=start+nb_col
    A_bloc=A[:,start:end]
    u_bloc=u[start:end]
    v_bloc=np.dot(A_bloc,u_bloc)

    
    if rank >0: 
        comm.send(v_bloc,0)
    
    if rank ==0 :
        v = np.array(v_bloc)
        for k in range (1,size):
            received = comm.recv(source=k)
            v+=received
        fin = time()
        print (f"{rank} : Le temps en découpant par colonne est {fin-deb}")
        return v

def produit_ligne(A,u): 
    nb_line=dim//size 
    
    deb= time()
    start=rank*nb_line
    end=start+nb_line
    A_bloc=A[start:end,:]
    v_bloc=np.dot(A_bloc,u)
    

    if rank >0: 
        comm.send(v_bloc,0)
        
    
    if rank ==0 :
        v = np.array(v_bloc)
        for k in range (1,size):
            received = comm.recv(source=k)
            v=np.append(v,received)
        fin = time()
        print (f"Le temps en découpant par ligne est {fin-deb}")
        return(v)

if rank >0 :
    print(f"{rank} : \n")
    classique=produit_classique(A,u)
    lignes=produit_ligne(A,u)
    colonnes=produit_colonne(A,u)
    print(f"\n")

if rank ==0:
    print(f"{rank} :")
    classique=produit_classique(A,u)
    lignes=produit_ligne(A,u)
    colonnes=produit_colonne(A,u)
    print(f"\n")
