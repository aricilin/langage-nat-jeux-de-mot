import json
import ast
import pull_dump



"""
open (f"data/JSON/element/{A}.JSON",'r',encoding='utf-8')as feA,open (f"data/JSON/element/{B}.JSON",'r',encoding='utf-8')as feB,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frA,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frB
"""
relationTransitive = ["r_lieu","r_lieu-1","r_isa","r_holo","r_hypo", "r_has_part","r_own","r_own-1","r_product_of","r_similar"]
idTransitive =["15","28","6","10","8","9","121","122","54","67"]
# inverselist = {"r_agent": "r_agent-1","r_agent-1": "r_agent", "r_patient": "r_patient-1", "r_patient": "r_patient-1" ,"r_isa": "r_hypo","r_hypo": "r_isa" ,"r_holo": "r_has_part", "r_has_part": "r_holo","r_lieu": "r_lieu-1", "r_lieu-1": "r_lieu"}

def nom(source,id):#renvoie le nom d'un element en utilisant son id et une base JSON
    with open (f"data/JSON/element/{source}.JSON",'r',encoding='utf-8')as feA:
        eA=json.loads(feA.read())
        for e in eA:
            if e['e']==id:
                return e['nom']
def relnom(r):#renvoie le nom d'une relation rt en partant de son id
    with open ("data/rt.JSON",'r',encoding='utf-8')as fsource:
        source=json.loads(fsource.read())
        for e in source:
            if e['r']==r:
                return e['nom']
            
def relid(nom):#renvoie l'id d'une relation rt en partant de son nom
    with open ("data/rt.JSON",'r',encoding='utf-8')as fsource:
        source=json.loads(fsource.read())
        for e in source:
            if e['nom']==nom:
                return e['r']


def deduction(A,B,R,liste):
    with open (f"data/JSON/element/{A}.JSON",'r',encoding='utf-8')as feA,open (f"data/JSON/element/{B}.JSON",'r',encoding='utf-8')as feB,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frA,open (f"data/JSON/relation/{B}.JSON",'r',encoding='utf-8')as frB:
        
        eA=json.loads(feA.read())
        eB=json.loads(feB.read())
        rA=json.loads(frA.read())
        rB=json.loads(frB.read())
        
        deduclist=[]
        
        #on recupere les id des elements a comparer
        idA=eA[0]['e']
        idB=eB[0]['e']
        deduclist.append(idB)
        nb=0
        
        for r1 in rA:
            if r1['e1']==idA and r1['r'] in idTransitive : # A is a C non-absurde
                for r2 in rB :
                    if nb<5:
                        if r2['e1']== r1['e2'] and r2['r']==R and r2['e1'] not in deduclist :# C relation B
                            inter = nom(A,r1['e2'])
                            liste.append((ast.literal_eval(f"{(A,relnom(r1['r']),inter),(inter,relnom(r2['r']),B)}"),f"({r1['w']},{r2['w']})"))
                            deduclist.append(r2['e1'])
                            nb+=1
                   

def direct(A,B,R):
    with open (f"data/JSON/element/{A}.JSON",'r',encoding='utf-8')as feA,open (f"data/JSON/element/{B}.JSON",'r',encoding='utf-8')as feB,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frA:
        
        eA=json.loads(feA.read())
        eB=json.loads(feB.read())
        rA=json.loads(frA.read())


        idA=eA[0]['e']
        idB=eB[0]['e']

        for r1 in rA:
             if r1['e1']==idA and r1['e2']==idB and r1['r']==R and int(r1['w'])>0:
                print(f"({A}, {relnom(R)}, {B}) <== direct  ")
                
def induction(A,B,R,liste):
    with open (f"data/JSON/element/{A}.JSON",'r',encoding='utf-8')as feA,open (f"data/JSON/element/{B}.JSON",'r',encoding='utf-8')as feB,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frA,open (f"data/JSON/relation/{B}.JSON",'r',encoding='utf-8')as frB:
        eA=json.loads(feA.read())
        eB=json.loads(feB.read())
        rA=json.loads(frA.read())
        rB=json.loads(frB.read())
        induclist=[]
        

        #on recupere les id des elements a comparer
        idA=eA[0]['e']
        idB=eB[0]['e']
        induclist.append(idB)
        nb=0
     
        for r1 in rA:
            if r1['e2']==idA and r1['r'] in idTransitive : # C is a A non-absurde
                for r2 in rB :
                    if nb<5:
                        if r2['e1']== r1['e2'] and r2['r']==R and r2['e1']not in induclist :# C relation B
                            inter = nom(A,r1['e1'])
                            liste.append((ast.literal_eval(f"{(inter,relnom(r1['r']),A),(inter,relnom(r2['r']),B)}"),f"({r1['w']},{r2['w']})"))
                            induclist.append(r2['e1'])
                            nb+=1
                            
               
# def transitivite(A,B,R,liste,cpt=2,temp=[],deduclist=[]):
#     with open (f"data/JSON/element/{A}.JSON",'r',encoding='utf-8')as feA,open (f"data/JSON/element/{B}.JSON",'r',encoding='utf-8')as feB,open (f"data/JSON/relation/{A}.JSON",'r',encoding='utf-8')as frA,open (f"data/JSON/relation/{B}.JSON",'r',encoding='utf-8')as frB:
        
#         eA=json.loads(feA.read())
#         eB=json.loads(feB.read())
#         rA=json.loads(frA.read())
#         rB=json.loads(frB.read())
        
        
#         #on recupere les id des elements a comparer
#         idA=eA[0]['e']
#         idB=eB[0]['e']
#         deduclist.append(idB)
#         nb=0
#         if cpt >0:
#             for r1 in rA:
#                 if r1['e1']==idA and r1['r'] in idTransitive and r1['e2'] not in deduclist : # A is a C non-absurde
#                     for r2 in rB :
#                         if nb<5:
#                             inter = nom(A,r1['e2'])
#                             temp.append((ast.literal_eval(f"{(A,relnom(r1['r']),inter),(inter,relnom(r2['r']),B)}"),f"({r1['w']},{r2['w']})"))
#                             deduclist.append(r2['e1'])
#                             nb+=1
#                             pull_dump.import_jdm(inter)
#                             inter=pull_dump.testname(inter)
#                             transitivite(inter,B,R,liste,cpt-1,temp,deduclist)
#                             print(inter)
        
            

def recherche(A,B,R,liste):
    A=pull_dump.testname(A)
    B=pull_dump.testname(B)
    direct(A,B,R)
    deduction(A,B,R,liste)
    induction(A,B,R,liste)
    # transitivite(A,B,R,liste)