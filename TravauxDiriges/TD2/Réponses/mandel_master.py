# Calcul de l'ensemble de Mandelbrot en python
import numpy as np
from dataclasses import dataclass
from PIL import Image
from math import log
from time import time
import matplotlib.cm
from mpi4py import MPI
comm = MPI.COMM_WORLD

@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius:  float = 2.0

    def __contains__(self, c: complex) -> bool:
        return self.stability(c) == 1

    def convergence(self, c: complex, smooth=False, clamp=True) -> float:
        value = self.count_iterations(c, smooth)/self.max_iterations
        return max(0.0, min(value, 1.0)) if clamp else value

    def count_iterations(self, c: complex,  smooth=False) -> int | float:
        z:    complex
        iter: int

        # On vérifie dans un premier temps si le complexe
        # n'appartient pas à une zone de convergence connue :
        #   1. Appartenance aux disques  C0{(0,0),1/4} et C1{(-1,0),1/4}
        if c.real*c.real+c.imag*c.imag < 0.0625:
            return self.max_iterations
        if (c.real+1)*(c.real+1)+c.imag*c.imag < 0.0625:
            return self.max_iterations
        #  2.  Appartenance à la cardioïde {(1/4,0),1/2(1-cos(theta))}
        if (c.real > -0.75) and (c.real < 0.5):
            ct = c.real-0.25 + 1.j * c.imag
            ctnrm2 = abs(ct)
            if ctnrm2 < 0.5*(1-ct.real/max(ctnrm2, 1.E-14)):
                return self.max_iterations
        # Sinon on itère
        z = 0
        for iter in range(self.max_iterations):
            z = z*z + c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iter + 1 - log(log(abs(z)))/log(2)
                return iter
        return self.max_iterations


def mandelbrotRow(width, height, num_ligne):
    pixels = np.empty(width, dtype=np.double)
    scaleX = 3./width
    scaleY = 2.25/height
    for j in range (0, width):
        c = complex(-2. + scaleX*j, -1.125 + scaleY * num_ligne)
        pixels[j] = mandelbrot_set.convergence(c, smooth=True)
    return pixels


def calculeMandelbrotSet(width, height, rank, size):
    row = np.empty(width, dtype=np.double)
    deb_loc = time()
    pixels = np.empty((width, height), dtype=np.double)

    #print(f"enter the loop ")
    
    if rank == 0:
        #print(f"start")
        
        irow = 0
        for i in range (1, size):
            comm.send(irow, dest = i, tag = 101)
            irow += 1
            #print(f"Envoie de la première ligne au process {i}")
        
        while (irow < height):
            status = MPI.Status()
            #print("attente")
            #Attente du résultat d'un esclave
            comm.Recv(row, status=status)
            #print(f"message reçu de {sender}")
            
            #row = comm.recv(source = MPI.ANY_SOURCE, tag= MPI.ANY_TAG, status=status)
            sender = status.Get_source()
            jrow = status.Get_tag()
            

            #Envoie d'une nouvelle ligne à calculer
            comm.send(irow, dest= sender, tag = 101)
            #print(f"message envoyé à {sender}")

            #Copie les données reçues 
            pixels[:, height - jrow -1] = row 

            irow += 1
            #print(f"irow = {irow}")

        irow = -1

        #On reçoit les lignes
        for p in range (1, size):
            status = MPI.Status()

            comm.Recv(row, status=status)
            #row = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
            sender = status.Get_source()
            jrow = status.Get_tag()
            
            comm.send(irow, dest=sender, tag=101)
            pixels[:, height - jrow - 1] = row

    else : 
        while True:
            irow = 0
            irow = comm.recv( source = 0, tag = 101)
            #print(f"Reçoit la première ligne pour le process {rank}")

            if irow != -1:
                row = mandelbrotRow(width, height, irow)
                #print("ok")
                comm.Send(row, dest = 0, tag = irow)
                #print(f"Envoie de la ligne {irow}")
            else : 
                break
    
    fin_loc = time()
    print(f"Temps de calcul de l'ensemble de Mandelbrot numéro {rank} sur {size} : {fin_loc - deb_loc}")
    return pixels


# On peut changer les paramètres des deux prochaines lignes
mandelbrot_set = MandelbrotSet(max_iterations=50, escape_radius=10)
width, height = 1024, 1024

rank = comm.Get_rank()
size = comm.Get_size()

print(f"rank : {rank}, size : {size}")

convergence = np.empty((width, height), dtype=np.double)
pixels = calculeMandelbrotSet(width, height, rank, size)



if rank ==0 : 
    
    

    #construction de l'image
    deb = time()
    image = Image.fromarray(np.uint8(matplotlib.cm.plasma(pixels.T)*255))
    fin = time()
    print(f"Temps de constitution de l'image : {fin-deb}")
    image.show()
