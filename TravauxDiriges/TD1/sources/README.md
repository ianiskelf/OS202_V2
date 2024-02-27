
# TD1

`pandoc -s --toc README.md --css=./github-pandoc.css -o README.html`

## lscpu

Architecture:            x86_64
  CPU op-mode(s):        32-bit, 64-bit
  Address sizes:         48 bits physical, 48 bits virtual
  Byte Order:            Little Endian
CPU(s):                  8
  On-line CPU(s) list:   0-7
Vendor ID:               AuthenticAMD
  Model name:            AMD Ryzen 5 3500U with Radeon Vega Mobile Gfx
    CPU family:          23
    Model:               24
    Thread(s) per core:  2
    Core(s) per socket:  4
    Socket(s):           1
    Stepping:            1
    BogoMIPS:            4191.93
Caches (sum of all):     
  L1d:                   128 KiB (4 instances)
  L1i:                   256 KiB (4 instances)
  L2:                    2 MiB (4 instances)
  L3:                    4 MiB (1 instance)

## Produit matrice-matrice



### Permutation des boucles

*Expliquer comment est compilé le code (ligne de make ou de gcc) : on aura besoin de savoir l'optim, les paramètres, etc. Par exemple :*

`make TestProduct.exe && ./TestProduct.exe 1024`


  ordre           | time    | MFlops  | MFlops(n=2048) 
------------------|---------|---------|----------------
i,j,k (origine)   | 2.73764 | 782.476 | 108.26           
j,i,k             | 0.849051 | 2529.27 | 329.936
i,k,j             | 6.1705 | 348.024 | 129.109
k,i,j             | 31.421  | 62.0361  | 70.3662  
j,k,i             | 0.795297 | 2700.23 | 2828.6   
k,j,i             | 0.849051 | 2529.27 | 2191.71

*Discussion des résultats*



### OMP sur la meilleure boucle 

`make TestProduct.exe && OMP_NUM_THREADS=8 ./TestProduct.exe 1024`

  OMP_NUM         | MFlops(n=512) | MFlops(n=1024)  | MFlops(n=2048) | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
1 | 1449.7 | 1299.8 | 1300.1 | 1178.3 |
2                 | 1534.5 | 1269.5 | 1133.8 | 1316.2
3 | 1456.9 | 1041.5 | 999.1 | 1190.0
4 | 1558.3 | 1280.8 | 1154.9 | 1258.3
5 | 1489.2 | 1330.5 | 1287.5 | 1246.3
6 | 1579.1 | 1427.5 | 1290.8 | 1244.7
7 | 1535.0 | 1325.8 | 1235.5 | 1154.9
8 | 1591.0 | 1361.8 | 1210.5 | 1236.5


### Produit par blocs

`make TestProduct.exe && ./TestProduct.exe 1024`

  szBlock         | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)
------------------|---------|----------------|----------------|---------------
origine (=max)    |  |
32                |  |
64                |  |
128               |  |
256               |  |
512               |  | 
1024              |  |




### Bloc + OMP



  szBlock      | OMP_NUM | MFlops  | MFlops(n=2048) | MFlops(n=512)  | MFlops(n=4096)|
---------------|---------|---------|-------------------------------------------------|
A.nbCols       |  1      |         |                |                |               |
512            |  8      |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|
Speed-up       |         |         |                |                |               |
---------------|---------|---------|-------------------------------------------------|



### Comparaison with BLAS


# Tips 

```
	env 
	OMP_NUM_THREADS=4 ./produitMatriceMatrice.exe
```

```
    $ for i in $(seq 1 4); do elap=$(OMP_NUM_THREADS=$i ./TestProductOmp.exe|grep "Temps CPU"|cut -d " " -f 7); echo -e "$i\t$elap"; done > timers.out
```
