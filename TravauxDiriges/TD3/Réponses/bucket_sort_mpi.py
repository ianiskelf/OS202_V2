from mpi4py import MPI
import numpy as np
from time import time
import utils
import constants

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

elements = []
buckets = []

start_time = time()

# Processes need to initialize empty lists
if rank == 0:
    elements = utils.generate_random(size=constants.N_ELEMENTS, high=constants.MAX_VALUE)
    print(f"Original array : {elements}")

    buckets = utils.split_array(elements, size)
    print(f"Buckets : {buckets}")

# Scatter les buckets en différents processes
buckets = comm.scatter(buckets, root=0)

# Tri dans chaque bucket
buckets = utils.insertion_sort(buckets)
print(f"Rank {rank}, sorted bucket : {buckets}")

# Gather buckets
buckets = comm.gather(buckets, root=0)

if rank == 0:
    sorted_buckets = np.concatenate(buckets)
    print(f"Sorted array : {sorted_buckets}")

    end_time = time()
    execution_time = end_time - start_time
    print(f"Execution time : {execution_time}")
