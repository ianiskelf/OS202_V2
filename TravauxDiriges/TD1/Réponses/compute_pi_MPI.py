# Calcul pi par une méthode stochastique (convergence très lente !)
import time
import numpy as np
from mpi4py import MPI

globCom = MPI.COMM_WORLD.Dup()
nbp     = globCom.size
rank    = globCom.rank
name    = MPI.Get_processor_name()

# Nombre d'échantillons :
nb_samples = 5_000_000

beg = time.time()
# Tirage des points (x,y) tirés dans un carré [-1;1] x [-1; 1]
x = 2.*np.random.random_sample((nb_samples,))-1.
y = 2.*np.random.random_sample((nb_samples,))-1.
# Création masque pour les points dans le cercle unité
filtre = np.array(x*x + y*y < 1.)
# Compte le nombre de points dans le cercle unité
sum = np.add.reduce(filtre, 0)


if rank != 0:
    globCom.send(sum, dest=0, tag=1)


if rank == 0:
    for i in range(1, nbp):
        data = globCom.recv(source=i, tag=1)
        sum += data
    approx_pi = 4.*sum/(nb_samples*nbp)
    end = time.time()
    print(f"Temps pour calculer pi : {end - beg} secondes")
    print(f"Pi vaut environ {approx_pi}")


