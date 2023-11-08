import pull_dump,recherche
from timeit import default_timer as timer

from sys import argv

start=timer()
pull_dump.import_jdm(argv[1])
pull_dump.import_jdm(argv[3])
rel=recherche.relid(argv[2])
data=[]
recherche.recherche(argv[1],argv[3],rel,data)
nb=0
data.sort(key=lambda tup: tup[1][0], reverse=True) # ordre décroissant de poids

for tuple in data:
        # print (tuple)
        if nb<5:
            print(f"({argv[1]}, {recherche.relnom(rel)}, {argv[3]}) <== ",end="")
            for i in range (len(tuple[0])):  
                if i != len(tuple[0][i])-2:
                    print(f"{tuple[0][i]} & ",end='')
                else:
                    print(f"{tuple[0][i]} poids {tuple[1]} ")
            nb+=1
        # if nb > 10:
        #      break
if len(data)==0:
     print("c'est non")
end=timer()
print(f"{end - start} secondes")
