import numpy as np
import math as math
import matplotlib.pyplot as plt

class SparseMatrix:

    def __init__(self, fromiter, shape):
        n, m = shape
        self.shape = shape
        self.n = n
        self.m = m
        self.nnz = 0 # TODO: nombre de valeurs non-nulles
        self.rowptr = [0] # liste de taille n + 1 des intervalles des colonnes, commence a 0
        self.colind = [] # liste de taille nnz des indices des valeurs non-nulles
        
        self.data = [] # liste de taille nnz des valeurs non-nulles
        
        for i,e in enumerate(fromiter):#Chaque range de la matrice
            nombre_valeurs_range=0 #Compteur pour utiliser le nombre de laveurs sur la range
            for j,f in enumerate(e):#Chaque valeur de la range de la matrice
                if(f != 0):#valeur != 0
                    nombre_valeurs_range += 1 
                    self.nnz += 1
                    self.colind.append(j)#On ajoute les indice de colonnes correxpondant aux valeurs 
                    self.data.append(f)#On ajoute la valeur dans le tableau des valeurs
            self.rowptr.append((self.rowptr[len(self.rowptr)-1]+nombre_valeurs_range)) # valeur precedente de rowptr + nombre valeurs sur range
        self.epars = [self.rowptr, self.colind, self.data]
             
    def __getitem__(self, k): 
        
        i, j = k # i est la colonne, j la range
            
        indices_range = range(self.rowptr[i], self.rowptr[i+1])#contient les indices de colind et data où les colonnes et les valeurs non-nulles de la rangée i sont stockées.
                
        while indices_range:
            k = math.floor(len(indices_range)/2)
            if self.colind[indices_range[k]] is j:
                return self.data[indices_range[k]] # Pours toutes les valeurs non nulles, nous verifions si la colonne est pour cette range a une valeur. si oui, on la retourne
            elif self.colind[indices_range[k]] > j:# Si non, nous continuons, utilisant le sous tableau de tous les elemetns plus petits que j
                indices_range = indices_range[0:math.floor(len(indices_range)/2)]
            elif self.colind[indices_range[k]] < j:# Si non, nous continuons, utilisant le sous tableau de tous les elemetns plus grands que j
                indices_range = indices_range[math.ceil(len(indices_range)/2):len(indices_range)]
                
        return 0  # Si non, on retourne 0
    
    def todense(self):
        
        nombre_elements_matrice = 1
        for i in self.shape :
            nombre_elements_matrice *= i # Nous cherchons le nombre d'elements total dans la structure
        
        dense = self.data[:] #tableau des valeurs non 0 # toutes les valeurs non nulles 
        data_count = 0 # Toutes les valeurs non nulle vues dans l'iteration
        horizontal_count = 0 # compteru de distance parcouru sur la dimension i
        vertical_count = 0 # compteur de distance parcouru sur la dimension j
        line_count = self.rowptr[vertical_count+1]-self.rowptr[vertical_count] # nombres de valeurs sur la ligne de la dimension i
        
        while len(dense) < nombre_elements_matrice :# Nous commencons avec touts les elements non nuls et placons des 0 aux bon endroits. Nous arretons lorsque le nombre d'elements dans le la liste est egale au nombre d'elements attendus dans la structure finale
            if data_count is not len(self.data):
                if (horizontal_count is self.m) :# nous iterons sur les dimensions de la structure finale, en restant en 1D. Ici, nous sommes au bout de la ligne
                    horizontal_count = 0
                    vertical_count += 1                  
                    line_count = self.rowptr[vertical_count+1]-self.rowptr[vertical_count]
                elif (line_count is 0) or (horizontal_count < self.colind[data_count]) :#lorsqu'un zero devrait etre place
                    dense.insert(vertical_count*self.shape[1]+horizontal_count,0)
                    horizontal_count += 1

                elif horizontal_count is self.colind[data_count] :# Lorsque l'elements que nous regardons est non nul
                    horizontal_count += 1
                    line_count -= 1
                    data_count += 1
            else :# Lorsqu'il ne reste que des zeros a placer
                dense.insert(vertical_count*self.shape[1]+horizontal_count,0)
                horizontal_count += 0
        return np.reshape(dense,self.shape)# Nous retournons la structure avec les bonnes dimensions. 
        
    def __str__(self):
        str = ""   
        dictionnaire_variables = vars(self)  # Dictionnaire des variables de la classe
        for i in [*dictionnaire_variables]:  # Unpacking du dictionnaire des variables pour avoir une liste des cles  
            str += i + " :\n" + "%s\n\n" % (dictionnaire_variables[i],)  #  Valeur pour variable i avec vars(self)[i]. Nous utilisons le singleton pour imprimer le tuple de shape en addition aux autres 
        return str
    
    
    
class SparseTensor:

    def __init__(self, fromiter, shape):
        n, m, o = shape
        self.shape = shape
        self.n = n
        self.m = m
        self.o = o
        self.nnz = 0 # TODO: nombre de valeurs non-nulles
        self.rowptr = [0] # liste de taille n + 1 des intervalles des colonnes, commence a 0
        self.colind = [] # liste de taille nnz des indices des valeurs non-nulles
        self.data = [] # liste de taille nnz des valeurs non-nulles
        
        for g in fromiter:
            for i,e in enumerate(g):#Chaque range de la matrice
                nombre_valeurs_range=0 #Compteur pour utiliser le nombre de laveurs sur la range
                for j,f in enumerate(e):#Chaque valeur de la range de la matrice
                    if(f != 0):#valeur != 0
                        nombre_valeurs_range += 1 
                        self.nnz += 1
                        self.colind.append(j)#On ajoute les indice de colonnes correxpondant aux valeurs 
                        self.data.append(f)#On ajoute la valeur dans le tableau des valeurs
                self.rowptr.append((self.rowptr[len(self.rowptr)-1]+nombre_valeurs_range)) # valeur precedente de rowptr + nombre valeurs sur range
        self.epars = [self.rowptr, self.colind, self.data]
             
    def __getitem__(self, k): 
        
        i, j, h = k # i est la colonne, j la range
            
        indices_range = range(self.rowptr[i+self.n*h], self.rowptr[i+self.n*h+1])#contient les indices de colind et data où les colonnes et les valeurs non-nulles de la rangée i sont stockées.
                
        while indices_range:
            k = math.floor(len(indices_range)/2)
            if self.colind[indices_range[k]] is j:
                return self.data[indices_range[k]] # Pours toutes les valeurs non nulles, nous verifions si la colonne est pour cette range a une valeur. si oui, on la retourne
            elif self.colind[indices_range[k]] > j:# Si non, nous continuons, utilisant le sous tableau de tous les elemetns plus petits que j
                indices_range = indices_range[0:math.floor(len(indices_range)/2)]
            elif self.colind[indices_range[k]] < j:# Si non, nous continuons, utilisant le sous tableau de tous les elemetns plus grands que j
                indices_range = indices_range[math.ceil(len(indices_range)/2):len(indices_range)]
                
        return 0  # Si non, on retourne 0
    
    def todense(self):
        
        nombre_elements_matrice = 1
        for i in self.shape :
            nombre_elements_matrice *= i # Nous cherchons le nombre d'elements total dans la structure
        
        dense = self.data[:] #tableau des valeurs non 0 # toutes les valeurs non nulles 
        data_count = 0 # Toutes les valeurs non nulle vues dans l'iteration
        horizontal_count = 0 # compteru de distance parcouru sur la dimension i
        vertical_count = 0 # compteur de distance parcouru sur la dimension j
        line_count = self.rowptr[vertical_count+1]-self.rowptr[vertical_count] # nombres de valeurs sur la ligne de la dimension i
        
        while len(dense) < nombre_elements_matrice :# Nous commencons avec touts les elements non nuls et placons des 0 aux bon endroits. Nous arretons lorsque le nombre d'elements dans le la liste est egale au nombre d'elements attendus dans la structure finale
            if data_count is not len(self.data):
                if (horizontal_count is self.m) :# nous iterons sur les dimensions de la structure finale, en restant en 1D. Ici, nous sommes au bout de la ligne
                    horizontal_count = 0
                    vertical_count += 1                  
                    line_count = self.rowptr[vertical_count+1]-self.rowptr[vertical_count]
                elif (line_count is 0) or (horizontal_count < self.colind[data_count]) :#lorsqu'un zero devrait etre place
                    dense.insert(vertical_count*self.shape[1]+horizontal_count,0)
                    horizontal_count += 1

                elif horizontal_count is self.colind[data_count] :# Lorsque l'elements que nous regardons est non nul
                    horizontal_count += 1
                    line_count -= 1
                    data_count += 1
            else :# Lorsqu'il ne reste que des zeros a placer
                dense.insert(vertical_count*self.shape[1]+horizontal_count,0)
                horizontal_count += 0
        return np.reshape(dense,self.shape[::-1])# Nous retournons la structure avec les bonnes dimensions. 
        
    def __str__(self):
        str = ""   
        dictionnaire_variables = vars(self)  # Dictionnaire des variables de la classe
        for i in [*dictionnaire_variables]:  # Unpacking du dictionnaire des variables pour avoir une liste des cles  
            str += i + " :\n" + "%s\n\n" % (dictionnaire_variables[i],)  #  Valeur pour variable i avec vars(self)[i]. nous utilisons le singleton pour imprimer le tuple de shape aussi
        return str
