from mpi4py import MPI
import time
import numpy as np


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

jeton = None

#Initialisation temps
beg = time.time()

if rank == 0:
    jeton = 1
    
    dest_rank = (rank + 1) % size
    comm.send(jeton, dest=dest_rank)
    
    jeton = comm.recv(source=size - 1)
    
    print(f"Process {rank} reçoit le jeton {jeton} du process {size - 1}")
    end = time.time()
    print(f"\nTemps pour faire le tour : {end - beg} secondes")

# Les autres process reçoivent le jeton du process précédent et la passe au suivant après l'avoir incrémenté
else:
    source_rank = (rank - 1) % size
    jeton = comm.recv(source=source_rank)
    
    print(f"Process {rank} reçoit le jeton {jeton} du process {(rank - 1) % size}")

    jeton += 1

    dest_rank = (rank + 1) % size
    comm.send(jeton, dest=dest_rank)

MPI.Finalize()
