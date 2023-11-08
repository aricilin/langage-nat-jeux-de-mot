import json,ast

liste=[]
with open ("data/rt.txt","r",encoding='utf-8' ) as file, open ("data/rt.JSON","w",encoding='utf-8' ) as fout:
    for line in file:
        els = line.split('|')
        liste.append({
            "r":els[0].split('=')[1],
            "nom":ast.literal_eval(els[1].split('=')[1])
            })

    element_json=json.dumps(liste,indent=1)
    fout.write(element_json)