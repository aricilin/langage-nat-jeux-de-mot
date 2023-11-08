import requests
import json
import os, shutil
def testname(name):
    temp =name
    try:
        temp=f"{name.split('>')[0]}__{name.split('>')[1]}"
    except IndexError:
        return name
    return temp
def importer(terme,val=-1):
    base="https://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel="

    "chat&rel=6"
    requete = base + terme

    if val!=-1:
        requete += "&rel=" + val
    

    r=requests.get(requete).text
    terme=testname(terme)
    f= open(f"data/dump/{terme}.txt","w",encoding='utf8')
    f.write(r)

    f.close()


def convertir(fichier):
    filepath = fichier
    
    filename = filepath.split('/')[len(filepath.split('/'))-1]
    
    name=testname(filename)
    filepath=f"data/dump/{name}"
    name=f"{filename.split('.')[0]}.JSON"
    infile= open(filepath,"r",encoding='utf8')

    filename = filepath.split('/')[len(filepath.split('/'))-1]
    name=f"{filename.split('.')[0]}.JSON"
    
    relationout = open(f"data/JSON/relation/{name}","w",encoding='utf8') 

    elemout =open(f"data/JSON/element/{name}","w",encoding='utf8')


    relations=[]
    elemenents=[]
    for line in infile:
        match line.split(';')[0]:
            case "e":
                # example e;150;'chat';1;5483
                elemenents.append({
                    "e":line.split(';')[1],
                    "nom":f"""{line.split("'")[1]}"""
                })
            case"r":
                #example r;14400314;150;436315;6;1073
                relations.append({
                    "e1":line.split(';')[2],
                    "r":line.split(';')[4],
                    "e2":line.split(';')[3],
                    "w":line.split(';')[5].splitlines()[0]
                    
                })

    element_json=json.dumps(elemenents,indent=1)
    elemout.write(element_json)
    relation_json=json.dumps(relations,indent=1)
    relationout.write(relation_json)

def empty_folder(target_folder):
    folder = target_folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def import_jdm(mot,val=-1):
    file_exists = os.path.exists(f"data/JSON/element/{mot}.JSON")
    if file_exists:
        return
    importer(mot)
    convertir(f"data/dump/{mot}.txt")
    empty_folder("data/dump")
