import numpy as np
import math as math
import matplotlib.pyplot as plt
from sparse import SparseMatrix
%matplotlib inline

# Importation des donnes MNIST
mnist_dataset = np.memmap('train-images-idx3-ubyte', offset=16, shape=(60000, 28, 28))

premiere_image = mnist_dataset[0].tolist() # first_image est de taille (28, 28)
encodage_premiere_image = SparseMatrix(premiere_image,(28,28))
premiere_image_encode_decode = encodage_premiere_image.todense()

plt.imshow(premiere_image, cmap='gray_r')
plt.show()
plt.imshow(encodage_premiere_image.todense(), cmap='gray_r')
plt.show()

# Comparaison Pixel par Pixel

pas_pareil = False
for i in range(len(premiere_image)):
    for j in range(len(premiere_image[i])):

        if premiere_image[i][j] != premiere_image_encode_decode[i][j]:
            print(premiere_image[i][j])
            print(premiere_image_encode_decode[i][j])
            print(i)
            print(j)
            print("\n")
            pas_pareil = True
        
if pas_pareil : 
    print("Les deux images ne sont pas identique")
else : 
    print("Les deux images sont identique")

encodage_mnist = SparseTensor(mnist_dataset,(28,28,60000))
encodage_mnist_dense = encodage_mnist.todense()

pas_pareil = False
for i in range(len(mnist_dataset)):
    for j in range(len(mnist_dataset[i])):
        for k in range(len(mnist_dataset[i][j])):
            if mnist_dataset[i][j][k] != encodage_mnist_dense[i][j][k]:
                print(mnist_dataset[i][j][k])
                print(encodage_mnist_dense[i][j][k])
                print(i)
                print(j)
                print(k)
                print("\n")
                pas_pareil = True
        
if pas_pareil : 
    print("Les deux images ne sont pas identique")
else : 
    print("Les deux images sont identique")