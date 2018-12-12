# encoding:utf-8

import heapq as hpg # queue uchun
from collections import defaultdict # listleri gostermek uchun
from tkinter import *
import tkinter

scaledversion = 1.5;

#Stackdaki elemetleri gosteren class
class QueueElementleri:

    def __init__(self):
        self.arraydakiler = []
        self.bashlangic = 0

    def elaveet(self, item, oncelik):
        hpg.heappush(self.arraydakiler, (oncelik, self.bashlangic, item))
        self.bashlangic += 1

    def silinecek(self):
        return hpg.heappop(self.arraydakiler)[-1]

    def egerBoshdursa(self):
        return len(self.arraydakiler) == 0

    def getSize(self):
        return self.bashlangic




# Node gostermek uchun class
class Node:

    # nodetapan - nodu tapir
    # "heuristik_cost" h(n)-dir hansi ki heurictic funksiyasi ile ishleyir
    # "heuristik_cost" A starin tapilmasinda istifade olunur: f(n) = g(n) + h(n) hansi ki

    def __init__(self, nodetapan, heuristik_cost):
        self.nodetapan = nodetapan
        self.heuristik_cost = heuristik_cost

    def Nodaget(self):
        return self.nodetapan

    def HeuristikCostTap(self):
        return self.heuristik_cost


# Graph gosteren bir class
class Graph:

    def __init__(self):
        self.nodlar = {} # nodlarin lughetini gosteren element
        self.edgeolanlar = [] # edge gosteren element
        self.yol = [] # gedilecek yol

        self.successors = defaultdict(list)


    # Edge elave eden funksiya
    def EdgeElaveEt(self, bashlangic, sonnoqte, uzunluq):
        edge = (bashlangic, sonnoqte, uzunluq) # tuple yaradir, 3 deneli
        if not self.EgerEdgevarsa(edge): # Eger edge yoxdursa elave edir
            self.nodlar[bashlangic], self.nodlar[sonnoqte] = bashlangic, sonnoqte # node elave edir
            self.edgeolanlar.append(edge) # edge elave edir
            self.successors[bashlangic.Nodaget()].append((sonnoqte, uzunluq)) # successor elave edir
        else:
            print('Error: edge (%s -> %s uzunluqlu %s) artıq var!' \
                % (edge[0].Nodaget(), edge[1].Nodaget(), edge[2]))


    # Edge olub olmadigini yoxlayan funksiya
    def EgerEdgevarsa(self, edge):
        for e in self.edgeolanlar:
            # bashlangic nodu ile son nodu yoxlayir
            if e[0].Nodaget() == edge[0].Nodaget() and \
                e[1].Nodaget() == edge[1].Nodaget() and e[2] == edge[2]:
                return True #eger duzdurse true verir
        return False #yoxsa false


    # Yolu gosteren funksiya
    def yoluTap(self):
        return self.yol


    # Esas A star algoritmasi
    def Astarfunksiyasi(self, bashlangic_noqte, son_noqte):
        if not self.edgeolanlar:
            print('Error: graph-da edge yoxdur!')
        else:
            # Her iki nodun olub olmamasin yoxlayir
            if bashlangic_noqte in self.nodlar and son_noqte in self.nodlar:
                if bashlangic_noqte == son_noqte: # Eger eynidirse
                    return 0

                queue = QueueElementleri() # queue duzeldir

                # "mesafe_vectoru" ve "pathquran" yolu yeniden qurmaq uchun ishlenir
                mesafe_vectoru, pathquran = {}, {}
                for node in self.nodlar:
                    mesafe_vectoru[node.Nodaget()] = None # none ile initialize olunur
                    pathquran[node.Nodaget()] = None
                mesafe_vectoru[bashlangic_noqte.Nodaget()] = 0

                # ne qeder cost var onu hesableyir : g(n) + h(n)
                g_cost, h_cost = 0, bashlangic_noqte.HeuristikCostTap()
                Astarcost = g_cost + h_cost
                queue.elaveet((bashlangic_noqte, g_cost, h_cost), Astarcost)
                umumi_cost = None

                while True:


                    hazirki_node, g_cost, h_cost = queue.silinecek()
                    successors = self.successors[hazirki_node.Nodaget()]

                    for successor in successors:
                        ensonnoqte, weight = successor

                        # Costlari hesablayir
                        yeni_g_cost = g_cost + weight
                        h_cost = ensonnoqte.HeuristikCostTap()
                        Astarcost = yeni_g_cost + h_cost
                        queue.elaveet((ensonnoqte, yeni_g_cost, h_cost), Astarcost)

                        #  "mesafe_vectoru" yenileyir
                        if mesafe_vectoru[ensonnoqte.Nodaget()]:
                            if mesafe_vectoru[ensonnoqte.Nodaget()] > yeni_g_cost:
                                mesafe_vectoru[ensonnoqte.Nodaget()] = yeni_g_cost
                                pathquran[ensonnoqte.Nodaget()] = hazirki_node.Nodaget()
                        else:
                            mesafe_vectoru[ensonnoqte.Nodaget()] = yeni_g_cost
                            pathquran[ensonnoqte.Nodaget()] = hazirki_node.Nodaget()

                        # neticeye chatmagi gosterir
                        if ensonnoqte.Nodaget() == son_noqte.Nodaget():
                            # umumi costu yenileyir
                            if not umumi_cost:
                                umumi_cost = Astarcost
                            elif Astarcost < umumi_cost:
                                umumi_cost = Astarcost

                    if queue.egerBoshdursa(): # Eger queue bosh deyilse
                        # Yolu yeniden qur
                        hazirki_node = son_noqte.Nodaget()
                        while hazirki_node:
                            self.yol.append(hazirki_node)
                            hazirki_node = pathquran[hazirki_node]
                        self.yol = self.yol[::-1]
                        return umumi_cost
            else:
                print('Error: Graph node təşkil eləmir!')


# tests ...
#Azerbaijani map
#Naxchivan
nodeSadarak = Node('Sadarak', 190)
nodeSharur = Node('Sharur', 180)
nodeBabak = Node('Babak', 170)
nodeCulfa = Node('Culfa', 160)
nodeOrdubad = Node('Ordubad', 130)
nodeShahbuz = Node('Shahbuz', 135)

nodeQazax = Node('Qazax', 454)
nodeAgstafa = Node('Agstafa', 442)
nodeTovuz = Node('Tovuz', 424)
nodeShamkir = Node('Shamkir', 385)
nodeGanja = Node('Ganja', 348)
nodeYevlax = Node('Yevlax', 280)
nodeAgdash = Node('Agdash', 265)
nodeBarda = Node('Barda', 305)
nodeTartar = Node('Tartar', 324)
nodeGoychay = Node('Goycay', 253)
nodeUcar = Node('Ucar', 235)
nodeZardab = Node('Zardab', 266)
nodeAghsu = Node('Aghsu', 153)
nodeKurdamir = Node('Kurdamir', 189)
nodeImishli = Node('Imishli', 258)
nodeQabala = Node('Qabala', 315)
nodeIsmayilli = Node('Ismayilli', 260)
nodeShamaxi = Node('Shamaxi', 116)
nodeGobustan = Node('Qobustan', 68)
nodeAbsheron = Node('Absheron', 90)
nodeHajigabul = Node('Hajigabul', 126)
nodeSabirabad = Node('Sabirabad', 176)
nodeSaatli = Node('Saatli', 191)
nodeBilasuvar = Node('Bilasuvar', 261)
nodeJalilabad = Node('Jalilabad', 211)
nodeSalyan = Node('Salyan', 127)
nodeNeftchala = Node('Neftchala', 185)
nodeAlibayramli = Node('Ali-Bayramli', 135)
nodeYardimli = Node('Yardimli', 292)
nodeMasalli = Node('Masalli', 236)
nodeLerik = Node('Lerik', 329)
nodeAstara = Node('Astara', 317)
nodeLankaran = Node('Lankaran', 272)
#Yuxari zona
nodeBalakan = Node('Balakan', 441)
nodeZagatala = Node('Zagatala', 318)
nodeQax = Node('Qax', 402)
nodeShaki = Node('Shaki', 352)
nodeOghuz = Node('Oghuz', 348)
nodeAghdam = Node('Aghdam', 379)
nodeKalbacar = Node('Kalbacar', 350)
nodeLachin = Node('Lachin', 414)
nodeXocali = Node('Xocali', 445)
nodeXocavend = Node('Xocavend', 425)
nodeFizuli = Node('Fizuli', 450)
nodeZangilan = Node('Zangilan', 465)

nodeQusar = Node('Qusar', 182)
nodeQuba = Node('Quba', 168)
nodeXachmaz = Node('Xachmaz', 161)
nodeSiyezen = Node('Siyezen', 105)
nodeXizi = Node('Xizi', 101)

nodeXirdalan = Node('Xirdalan', 16)
nodeSumqayit = Node('Sumqayit', 39)
nodeBaku = Node('Baku', 0)

graph = Graph()
#Naxchivan
graph.EdgeElaveEt(nodeSadarak, nodeSharur, 34)
graph.EdgeElaveEt(nodeSharur, nodeBabak, 71)
graph.EdgeElaveEt(nodeBabak, nodeShahbuz, 50)
graph.EdgeElaveEt(nodeBabak, nodeCulfa, 32)
graph.EdgeElaveEt(nodeCulfa, nodeOrdubad, 65)

#Ortalar - ARAN
graph.EdgeElaveEt(nodeQazax, nodeAgstafa, 50)
graph.EdgeElaveEt(nodeAgstafa, nodeTovuz, 45)
graph.EdgeElaveEt(nodeTovuz, nodeShamkir, 37)
graph.EdgeElaveEt(nodeShamkir, nodeGanja, 40)
graph.EdgeElaveEt(nodeGanja, nodeTartar, 84)
graph.EdgeElaveEt(nodeGanja, nodeYevlax, 69)
graph.EdgeElaveEt(nodeYevlax, nodeAgdash, 21)
graph.EdgeElaveEt(nodeYevlax, nodeBarda, 35)
graph.EdgeElaveEt(nodeTartar, nodeBarda, 21)
graph.EdgeElaveEt(nodeBarda, nodeAghdam, 51)
graph.EdgeElaveEt(nodeAgdash, nodeQabala, 76)
graph.EdgeElaveEt(nodeAgdash, nodeGoychay, 45)
graph.EdgeElaveEt(nodeQabala, nodeIsmayilli, 50)
graph.EdgeElaveEt(nodeGoychay, nodeIsmayilli, 59)
graph.EdgeElaveEt(nodeGoychay, nodeAghsu, 60)
graph.EdgeElaveEt(nodeGoychay, nodeUcar, 28)
graph.EdgeElaveEt(nodeUcar, nodeZardab, 49)
graph.EdgeElaveEt(nodeAghsu, nodeShamaxi, 36)
graph.EdgeElaveEt(nodeAghsu, nodeKurdamir, 31)
graph.EdgeElaveEt(nodeKurdamir, nodeImishli, 66)
graph.EdgeElaveEt(nodeIsmayilli, nodeShamaxi, 47)
graph.EdgeElaveEt(nodeIsmayilli, nodeAghsu, 69)
graph.EdgeElaveEt(nodeShamaxi, nodeGobustan, 153)
graph.EdgeElaveEt(nodeShamaxi, nodeAlibayramli, 110)
graph.EdgeElaveEt(nodeGobustan, nodeAlibayramli, 90)
graph.EdgeElaveEt(nodeShamaxi, nodeKurdamir, 68)
graph.EdgeElaveEt(nodeGobustan, nodeBaku, 91)

#Ashagi bolge
graph.EdgeElaveEt(nodeAstara, nodeLankaran , 45)
graph.EdgeElaveEt(nodeLankaran, nodeLerik , 53)
graph.EdgeElaveEt(nodeLankaran, nodeMasalli , 43)
graph.EdgeElaveEt(nodeMasalli, nodeJalilabad , 29)
graph.EdgeElaveEt(nodeMasalli, nodeYardimli , 55)
graph.EdgeElaveEt(nodeMasalli, nodeBilasuvar , 66)
graph.EdgeElaveEt(nodeBilasuvar, nodeSaatli , 95)
graph.EdgeElaveEt(nodeBilasuvar, nodeImishli , 71)
graph.EdgeElaveEt(nodeSaatli, nodeSabirabad , 33)
graph.EdgeElaveEt(nodeSaatli, nodeImishli , 32)
graph.EdgeElaveEt(nodeSabirabad, nodeKurdamir , 89)
graph.EdgeElaveEt(nodeSabirabad, nodeAlibayramli , 28)
graph.EdgeElaveEt(nodeAlibayramli, nodeHajigabul , 15)
graph.EdgeElaveEt(nodeSalyan, nodeNeftchala , 67)
graph.EdgeElaveEt(nodeSalyan, nodeAlibayramli , 42)
graph.EdgeElaveEt(nodeAlibayramli, nodeAbsheron , 133)
#graph.EdgeElaveEt(nodeMasalli, nodeLerik)

#Qarabagh zonasi
graph.EdgeElaveEt(nodeKalbacar, nodeLachin , 30)
graph.EdgeElaveEt(nodeLachin, nodeXocali , 30)
graph.EdgeElaveEt(nodeXocali, nodeAghdam , 30)
graph.EdgeElaveEt(nodeAghdam, nodeXocavend , 30)
graph.EdgeElaveEt(nodeXocavend, nodeFizuli , 30)
graph.EdgeElaveEt(nodeFizuli, nodeZangilan , 30)
graph.EdgeElaveEt(nodeFizuli, nodeImishli , 30)
graph.EdgeElaveEt(nodeZangilan, nodeImishli , 30)

#Yuxari zona
graph.EdgeElaveEt(nodeBalakan, nodeZagatala , 32)
graph.EdgeElaveEt(nodeZagatala, nodeQax , 48)
graph.EdgeElaveEt(nodeQax, nodeShaki , 41)
graph.EdgeElaveEt(nodeShaki, nodeOghuz , 42)
graph.EdgeElaveEt(nodeOghuz, nodeQabala , 51)

#Qusar-Baki
graph.EdgeElaveEt(nodeQusar, nodeQuba, 14)
graph.EdgeElaveEt(nodeQuba, nodeXachmaz, 27)
graph.EdgeElaveEt(nodeQuba,nodeSiyezen, 64)
graph.EdgeElaveEt(nodeSiyezen, nodeXizi, 60)
graph.EdgeElaveEt(nodeXizi, nodeSumqayit, 75)

graph.EdgeElaveEt(nodeXirdalan, nodeSumqayit , 24)
graph.EdgeElaveEt(nodeXirdalan, nodeBaku , 16)
graph.EdgeElaveEt(nodeSumqayit, nodeBaku , 39)

"""
def printfunction():
    umumi_cost = graph.Astarfunksiyasi(nodeQazax, nodeBaku) # executes the algorithm
    path = graph.yoluTap() # gets path

    if umumi_cost:
        print('Graph-ın ümumi costu: %s kilometrdir. Yol: %s ' % (umumi_cost, ' -> '.join(path)))

    else:
        print('Nəticə tapılmadı!')
printfunction()
"""
#Tkinter

master = Tk()

w = Canvas(master, width=1200, height=1080,bd=0,highlightthickness=0)
w.pack(expand = YES, fill = BOTH)
w.configure(bg="black")
master.minsize(width = 1200, height = 1080)
master.maxsize(width = 1920, height = 1080)
#w.pack()


w.create_line(scaledversion * 20,scaledversion*200,scaledversion* 40,scaledversion* 150, fill = "white", width = 2) #nodeAgstafa
w.create_text(scaledversion*35, scaledversion*145, anchor=W, font=("Purisa",10), text="Agstafa", fill = "white")
w.create_text(scaledversion*25, scaledversion*195, anchor=W, font=("Purisa",10), text="Qazax", fill = "white")
w.create_text(scaledversion*32, scaledversion*175, anchor = W, font=("Purisa",10), text="50", fill = "white")
w.create_oval(30,300,35,295, outline="white", fill="white", width=2)

w.create_line(scaledversion*40,scaledversion*150, scaledversion*80, scaledversion*200, fill = "white", width = 2) #Tovuz
w.create_text(scaledversion*75, scaledversion*185, anchor=W, font=("Purisa",10), text="Tovuz", fill = "white")
w.create_text(scaledversion*65, scaledversion*177, anchor = W, font=("Purisa",10), text="45", fill = "white")
w.create_oval(60,225,65,230, outline="white", fill="white", width=2)
w.create_oval(120,300,125,305, outline="white", fill="white", width=2)

w.create_line(scaledversion*80,scaledversion*200, scaledversion*130, scaledversion*190, fill = "white", width = 2) #Shamkir
w.create_text(scaledversion*130, scaledversion*185, anchor=W, font=("Purisa",10), text="Shamkir", fill = "white")
w.create_text(scaledversion*115, scaledversion*185, anchor = W, font=("Purisa",10), text="37", fill = "white")
w.create_oval(scaledversion*130, scaledversion*190,scaledversion*135, scaledversion*196, outline="white", fill="white", width=2)

w.create_line(scaledversion*130,scaledversion*190, scaledversion*160, scaledversion*210, fill = "white", width = 2) #ganja
w.create_text(scaledversion*160, scaledversion*205, anchor=W, font=("Purisa",10), text="Ganja", fill = "white")
w.create_text(scaledversion*140, scaledversion*205, anchor = W, font=("Purisa",10), text="40", fill = "white")
w.create_oval(scaledversion*160, scaledversion*210,scaledversion*164, scaledversion*215, outline="white", fill="white", width=2)

w.create_line(scaledversion*160,scaledversion*210, scaledversion*110 , scaledversion*300, fill = "white", width = 2) #Kalbacar
w.create_text(scaledversion*110, scaledversion*305, anchor=W, font=("Purisa",10), text="Kalbacar", fill = "white")
w.create_oval(scaledversion*110 , scaledversion*300,scaledversion*114 , scaledversion*304, outline="white", fill="white", width=2)

w.create_line(scaledversion*160,scaledversion*210, scaledversion*180, scaledversion*250, fill = "white",width = 2) #Tartar
w.create_text(scaledversion*160, scaledversion*255, anchor=W, font=("Purisa",10), text="Tartar", fill = "white")

w.create_line(scaledversion*180,scaledversion*250,scaledversion* 200,scaledversion* 260, fill = "white", width = 2) #Tartar-Barda
w.create_text(scaledversion*200, scaledversion*265, anchor=W, font=("Purisa",10), text="Barda", fill = "white")

w.create_line(scaledversion*160,scaledversion*210, scaledversion*190, scaledversion*210, fill = "white", width = 2) #Yevlax
w.create_text(scaledversion*190, scaledversion*205, anchor=W, font=("Purisa",10), text="Yevlax", fill = "white")

w.create_line(scaledversion*190,scaledversion*210,scaledversion* 200, scaledversion*260, fill = "white", width = 2) #Barda
w.create_text(scaledversion*200, scaledversion*255, anchor=W, font=("Purisa",10), text="Barda", fill = "white")

w.create_line(scaledversion*200,scaledversion*260, scaledversion*190, scaledversion*330, fill = "white", width = 2) #Barda - Agdam
w.create_text(scaledversion*190, scaledversion*325, anchor=W, font=("Purisa",10), text="Agdam", fill = "white")

w.create_line(scaledversion*190,scaledversion*210, scaledversion*210, scaledversion*230, fill = "white", width = 2) #Agdash
w.create_text(scaledversion*210,scaledversion* 225, anchor=W, font=("Purisa",10), text="Aghdash", fill = "white")

w.create_line(scaledversion*110, scaledversion*300, scaledversion*120, scaledversion*350, fill = "white", width = 2) #Lacin
w.create_text(scaledversion*120, scaledversion*345, anchor=W, font=("Purisa",10), text="Lacin", fill = "white")

w.create_line(scaledversion*120,scaledversion*350, scaledversion*160,scaledversion* 350, fill = "white", width = 2) #Xocali
w.create_text(scaledversion*160, scaledversion*345, anchor=W, font=("Purisa",10), text="Xocali", fill = "white")

w.create_line(scaledversion*160,scaledversion*350, scaledversion*190, scaledversion*330, fill = "white", width = 2) #Aghdam

w.create_line(scaledversion*190, scaledversion*330, scaledversion*210, scaledversion*360, fill = "white", width = 2) #nodeXocavend
w.create_text(scaledversion*210, scaledversion*355, anchor=W, font=("Purisa",10), text="Xocavend", fill = "white")

w.create_line(scaledversion*210,scaledversion*360, scaledversion*230, scaledversion*380, fill = "white", width = 2) #Fizuli
w.create_text(scaledversion*230, scaledversion*375, anchor=W, font=("Purisa",10), text="Fizuli", fill = "white")

w.create_line(scaledversion*230, scaledversion*380, scaledversion*220, scaledversion*430, fill = "white", width = 2) #Zangilan
w.create_text(scaledversion*220, scaledversion*435, anchor=W, font=("Purisa",10), text="Zangilan", fill = "white")

w.create_line(scaledversion*220,scaledversion*430, scaledversion*270, scaledversion*370, fill = "white", width = 2) #Imishli
w.create_text(scaledversion*270,scaledversion* 365, anchor=W, font=("Purisa",10), text="Imishli", fill = "white")

w.create_line(scaledversion*270,scaledversion*370, scaledversion*230, scaledversion*380, fill = "white", width = 2) #Imishli-nodeFizuli

w.create_line(scaledversion*270,scaledversion*370, scaledversion*280, scaledversion*320, fill = "white", width = 2) #Imisli - Kurdamir
w.create_text(scaledversion*280, scaledversion*315, anchor=W, font=("Purisa",10), text="Kurdamir", fill = "white")

w.create_line(scaledversion*280,scaledversion*320, scaledversion*245, scaledversion*305, fill = "white", width = 2) #Kurdamir - Zardab
w.create_text(scaledversion*245, scaledversion*300, anchor=W, font=("Purisa",10), text="Zardab", fill = "white")

w.create_line(scaledversion*280,scaledversion*320, scaledversion*230, scaledversion*260, fill = "white", width = 2) #Kurdamir-Ucar
w.create_text(scaledversion*230, scaledversion*255, anchor=W, font=("Purisa",10), text="Ucar", fill = "white")

w.create_line(scaledversion*245,scaledversion*305, scaledversion*230, scaledversion*260, fill = "white", width = 2) #Zardab - Ucar

w.create_line(scaledversion*230,scaledversion*260, scaledversion*240, scaledversion*220, fill = "white", width = 2) #Ucar - Goycay
w.create_text(scaledversion*240, scaledversion*215, anchor=W, font=("Purisa",10), text="Goycay", fill = "white")

w.create_line(scaledversion*240,scaledversion*220, scaledversion*210, scaledversion*230, fill = "white", width = 2) # Goycay-Agdash
w.create_text(scaledversion*210, scaledversion*225, anchor=W, font=("Purisa",10), text="Agdash", fill = "white")

w.create_line(scaledversion*210,scaledversion*230, scaledversion*250, scaledversion*210, fill = "white", width = 2) #Agdash-nodeQabala
w.create_text(scaledversion*250, scaledversion*205, anchor=W, font=("Purisa",10), text="Qabala", fill = "white")

w.create_line(scaledversion*250,scaledversion*210, scaledversion*230, scaledversion*180, fill = "white", width = 2) #Qabala-Oguz
w.create_text(scaledversion*230, scaledversion*175, anchor=W, font=("Purisa",10), text="Oghuz", fill = "white")

w.create_line(scaledversion*230,scaledversion*180,scaledversion* 200, scaledversion*170, fill = "white", width = 2) #Oguz-Seki
w.create_text(scaledversion*200, scaledversion*165, anchor=W, font=("Purisa",10), text="Sheki", fill = "white")

w.create_line(scaledversion*200,scaledversion*170,scaledversion* 160,scaledversion* 140, fill = "white", width = 2) #Seki- Qax
w.create_text(scaledversion*160, scaledversion*135, anchor=W, font=("Purisa",10), text="Qax", fill = "white")

w.create_line(scaledversion*160,scaledversion*140, scaledversion*150, scaledversion*120, fill = "white", width = 2) #Qax-Zaqatala
w.create_text(scaledversion*150, scaledversion*115, anchor=W, font=("Purisa",10), text="Zaqatala", fill = "white")

w.create_line(scaledversion*150,scaledversion*120, scaledversion*100, scaledversion*60, fill = "white", width = 2) #Zaqatala-Balakan
w.create_text(scaledversion*120, scaledversion*55, anchor=W, font=("Purisa",10), text="Balakan", fill = "white")

w.create_line(scaledversion*270,scaledversion*370, scaledversion*310, scaledversion*375, fill = "white", width = 2) #Imishli-Saatli
w.create_text(scaledversion*310, scaledversion*375, anchor=W, font=("Purisa",10), text="Saatli", fill = "white")

w.create_line(scaledversion*310, scaledversion*375, scaledversion*305, scaledversion*350, fill = "white", width = 2) #Saatli-Sabiarabad
w.create_text(scaledversion*305, scaledversion*350, anchor=W, font=("Purisa",10), text="Sabirabad", fill = "white")

w.create_line(scaledversion*305, scaledversion*350, scaledversion*340, scaledversion*330, fill = "white", width = 2) #Sabiarabad - Alibayramli
w.create_text(scaledversion*340, scaledversion*330, anchor=W, font=("Purisa",10), text="Alibayramli", fill = "white")

w.create_line(scaledversion*340, scaledversion*330, scaledversion*310, scaledversion*315, fill = "white", width = 2) #Alibayramli-Hajiqabul
w.create_text(scaledversion*310, scaledversion*315, anchor=W, font=("Purisa",10), text="Hajigabul", fill = "white")

w.create_line(scaledversion*340, scaledversion*330, scaledversion*345,scaledversion* 300, fill = "white", width = 2) #Alibayramli-Absheron
w.create_text(scaledversion*345, scaledversion*300, anchor=W, font=("Purisa",10), text="Absheron", fill = "white")

w.create_line(scaledversion*345, scaledversion*300, scaledversion*420, scaledversion*290, fill = "white", width = 2) #Absheron-baku
w.create_text(scaledversion*420, scaledversion*290, anchor=W, font=("Purisa",10), text="Baku", fill = "white")

w.create_line(scaledversion*420, scaledversion*290, scaledversion*360, scaledversion*360, fill = "white", width = 2) #baku-salyan
w.create_text(scaledversion*360, scaledversion*355, anchor=W, font=("Purisa",10), text="Salyan", fill = "white")

w.create_line(scaledversion*345, scaledversion*300,scaledversion* 320,scaledversion* 270, fill = "white", width = 2) #Absheron-qobustan
w.create_text(scaledversion*320, scaledversion*265, anchor=W, font=("Purisa",10), text="Qobustan", fill = "white")

w.create_line(scaledversion*320, scaledversion*270, scaledversion*290, scaledversion*240, fill = "white", width = 2) #qobustan-samaxi
w.create_text(scaledversion*290, scaledversion*235, anchor=W, font=("Purisa",10), text="Samaxi", fill = "white")

w.create_line(scaledversion*290, scaledversion*240, scaledversion*270, scaledversion*200, fill = "white", width = 2) #samaxi-ismayilli
w.create_text(scaledversion*270, scaledversion*195, anchor=W, font=("Purisa",10), text="Ismayilli", fill = "white")

w.create_line(scaledversion*360, scaledversion*230, scaledversion*320, scaledversion*270, fill = "white", width = 2) #sumqayit-qobustan
w.create_text(scaledversion*360, scaledversion*225, anchor=W, font=("Purisa",10), text="Sumqayit", fill = "white")

w.create_line(scaledversion*320, scaledversion*270, scaledversion*380, scaledversion*260, fill = "white", width = 2) #qobustan- xirdalan
w.create_text(scaledversion*380, scaledversion*255, anchor=W, font=("Purisa",10), text="Xirdalan", fill = "white")
w.create_line(scaledversion*320, scaledversion*270, scaledversion*260, scaledversion*280, fill = "white", width = 2)
w.create_line(scaledversion*290, scaledversion*240, scaledversion*260, scaledversion*280, fill = "white", width = 2)
w.create_line(scaledversion*270, scaledversion*200, scaledversion*240, scaledversion*220, fill = "white", width = 2) #ismayill-goycay
w.create_text(scaledversion*240, scaledversion*215, anchor=W, font=("Purisa",10), text="Goycay", fill = "white")

w.create_line(scaledversion*240, scaledversion*220, scaledversion*250,scaledversion* 210, fill = "white", width = 2) #ismayill-gabala

w.create_line(scaledversion*240, scaledversion*220, scaledversion*260,scaledversion* 280, fill = "white", width = 2) #ismayilli-agsu
w.create_text(scaledversion*260, scaledversion*275, anchor=W, font=("Purisa",10), text="Aghsu", fill = "white")

w.create_line(scaledversion*260, scaledversion*280, scaledversion*280,scaledversion* 320, fill = "white", width = 2) #agsu-kurdamir


w.create_line(scaledversion*420, scaledversion*290, scaledversion*380, scaledversion*260, fill = "white", width = 2) #baku xirdalan
w.create_line(scaledversion*380, scaledversion*260, scaledversion*360, scaledversion*230, fill = "white", width = 2) #xirdalan sumqayit
w.create_line(scaledversion*360, scaledversion*230, scaledversion*320, scaledversion*200, fill = "white", width = 2) #sumqayit-xizi
w.create_text(scaledversion*320, scaledversion*195, anchor=W, font=("Purisa",10), text="Xizi", fill = "white")

w.create_line(scaledversion*320, scaledversion*200, scaledversion*315, scaledversion*180, fill = "white", width = 2) #xizi-siyezen
w.create_text(scaledversion*315, scaledversion*185, anchor=W, font=("Purisa",10), text="Siyezen", fill = "white")

w.create_line(scaledversion*315, scaledversion*180, scaledversion*290, scaledversion*175, fill = "white", width = 2) #siyezen -quba
w.create_text(scaledversion*290, scaledversion*170, anchor=W, font=("Purisa",10), text="Quba", fill = "white")

w.create_line(scaledversion*290, scaledversion*175, scaledversion*310, scaledversion*150, fill = "white", width = 2) #quba-xacmaz
w.create_text(scaledversion*310, scaledversion*145, anchor=W, font=("Purisa",10), text="Xachmaz", fill = "white")

w.create_line(scaledversion*290, scaledversion*175, scaledversion*260, scaledversion*140, fill = "white", width = 2) #quba-qusar
w.create_text(scaledversion*260, scaledversion*140, anchor=W, font=("Purisa",10), text="Qusar", fill = "white")

w.create_line(scaledversion*340, scaledversion*330, scaledversion*360, scaledversion*360, fill = "white", width = 2) #Alibayramli-Salyan

w.create_line(scaledversion*360, scaledversion*360, scaledversion*375, scaledversion*390, fill = "white", width = 2) #Salyan-Neftcala
w.create_text(scaledversion*375, scaledversion*390, anchor=W, font=("Purisa",10), text="Neftcala", fill = "white")

w.create_line(scaledversion*360, scaledversion*360, scaledversion*350, scaledversion*420, fill = "white", width = 2) #salyan-Masalli
w.create_text(scaledversion*350, scaledversion*415, anchor=W, font=("Purisa",10), text="Masalli", fill = "white")

w.create_line(scaledversion*350, scaledversion*420, scaledversion*320, scaledversion*420, fill = "white", width = 2) #masalli-Jalilabad
w.create_text(scaledversion*310, scaledversion*415, anchor=W, font=("Purisa",10), text="Jalilabad", fill = "white")

w.create_line(scaledversion*350, scaledversion*420, scaledversion*315, scaledversion*440, fill = "white", width = 2) #masalli-yardimli
w.create_text(scaledversion*290, scaledversion*435, anchor=W, font=("Purisa",10), text="Yardimli", fill = "white")

w.create_line(scaledversion*350, scaledversion*420, scaledversion*340, scaledversion*450, fill = "white", width = 2) #masalli-lerik
w.create_text(scaledversion*320, scaledversion*455, anchor=W, font=("Purisa",10), text="Lerik", fill = "white")

w.create_line(scaledversion*350, scaledversion*420, scaledversion*370,scaledversion* 450, fill = "white", width = 2) #masalli-lankaran
w.create_text(scaledversion*370, scaledversion*285, anchor=W, font=("Purisa",10), text="Lankaran", fill = "white")

w.create_line(scaledversion*340, scaledversion*450, scaledversion*370, scaledversion*450, fill = "white", width = 2)
w.create_text(scaledversion*370, scaledversion*450, anchor=W, font=("Purisa",10), text="Lankaran", fill = "white")

w.create_line(scaledversion*370, scaledversion*450, scaledversion*350, scaledversion*480, fill = "white", width = 2) #lankrana-astara
w.create_text(scaledversion*360, scaledversion*480, anchor=W, font=("Purisa",10), text="Astara", fill = "white")


#Naxcivan
w.create_line(scaledversion*30,scaledversion*290, scaledversion*60, scaledversion*370, fill = "white", width = 2) #Sadarak - Sarur
w.create_text(scaledversion*30, scaledversion*285, anchor=W, font=("Purisa",10), text="Sadarak", fill = "white")
w.create_text(scaledversion*60, scaledversion*365, anchor=W, font=("Purisa",10), text="Sharur", fill = "white")

w.create_line(scaledversion*60,scaledversion*370,scaledversion* 80, scaledversion*390, fill = "white", width = 2) #Sarur Babak
w.create_text(scaledversion*80, scaledversion*386, anchor=W, font=("Purisa",10), text="Babak", fill = "white")

w.create_line(scaledversion*80,scaledversion*390, scaledversion*120,scaledversion* 370, fill = "white", width = 2) #Babak-Shahbuz
w.create_text(scaledversion*120, scaledversion*365, anchor=W, font=("Purisa",10), text="Shahbuz", fill = "white")

w.create_line(scaledversion*80,scaledversion*390, scaledversion*100, scaledversion*430, fill = "white", width = 2) #Babak-nodeCulfa
w.create_text(scaledversion*100, scaledversion*425, anchor=W, font=("Purisa",10), text="Culfa", fill = "white")

w.create_line(scaledversion*100,scaledversion*430, scaledversion*160,scaledversion* 480, fill = "white", width = 2) #Culfa-Ordubad
w.create_text(scaledversion*160, scaledversion*475, anchor=W, font=("Purisa",10), text="Ordubad", fill = "white")

#Heuristic Function
w.create_text(700,200, anchor=W, font=("Purisa",15), text="Heuristic Functions", fill = "white")
w.create_text(700,220, anchor=W, font=("Purisa",10), text="Sadarak = 0", fill = "white")
w.create_text(700,240, anchor=W, font=("Purisa",10), text="Sharur = 0", fill = "white")
w.create_text(700,260, anchor=W, font=("Purisa",10), text="Babak = 0", fill = "white")
w.create_text(700,280, anchor=W, font=("Purisa",10), text="Culfa = 0", fill = "white")
w.create_text(700,300, anchor=W, font=("Purisa",10), text="Ordubad = 0", fill = "white")
w.create_text(700,320, anchor=W, font=("Purisa",10), text="Shahbuz = 0", fill = "white")

w.create_text(700,340, anchor=W, font=("Purisa",10), text="Qazax = 454", fill = "white")
w.create_text(700,360, anchor=W, font=("Purisa",10), text="Agstafa = 442", fill = "white")
w.create_text(700,380, anchor=W, font=("Purisa",10), text="Tovuz = 424", fill = "white")
w.create_text(700,400, anchor=W, font=("Purisa",10), text="Shamkir = 385", fill = "white")
w.create_text(700,420, anchor=W, font=("Purisa",10), text="Ganja = 348", fill = "white")
w.create_text(700,440, anchor=W, font=("Purisa",10), text="Yevlax = 280", fill = "white")
w.create_text(700,460, anchor=W, font=("Purisa",10), text="Aghdash = 265", fill = "white")
w.create_text(700,480, anchor=W, font=("Purisa",10), text="Barda = 305", fill = "white")
w.create_text(700,500, anchor=W, font=("Purisa",10), text="Tartar = 324", fill = "white")
w.create_text(700,520, anchor=W, font=("Purisa",10), text="Goycay = 253", fill = "white")
w.create_text(700,540, anchor=W, font=("Purisa",10), text="Ucar = 235", fill = "white")
w.create_text(700,560, anchor=W, font=("Purisa",10), text="Zardab = 266", fill = "white")
w.create_text(700,580, anchor=W, font=("Purisa",10), text="Aghsu = 153", fill = "white")
w.create_text(700,600, anchor=W, font=("Purisa",10), text="Kurdamir = 189", fill = "white")
w.create_text(700,620, anchor=W, font=("Purisa",10), text="İmishli = 258", fill = "white")
w.create_text(700,640, anchor=W, font=("Purisa",10), text="İsmayıllı = 260", fill = "white")
w.create_text(700,660, anchor=W, font=("Purisa",10), text="Şamaxı = 116", fill = "white")
w.create_text(700,680, anchor=W, font=("Purisa",10), text="Qobustan = 68", fill = "white")
w.create_text(700,700, anchor=W, font=("Purisa",10), text="Abşeron = 90", fill = "white")
w.create_text(700,720, anchor=W, font=("Purisa",10), text="Hacıqabul = 126", fill = "white")
w.create_text(850,220, anchor=W, font=("Purisa",10), text="Sabirabad = 176", fill = "white")
w.create_text(850,240, anchor=W, font=("Purisa",10), text="Saatlı = 191", fill = "white")
w.create_text(850,260, anchor=W, font=("Purisa",10), text="Biləsüvar = 261", fill = "white")
w.create_text(850,280, anchor=W, font=("Purisa",10), text="Cəlilabad = 211", fill = "white")
w.create_text(850,300, anchor=W, font=("Purisa",10), text="Səlyan = 127", fill = "white")
w.create_text(850,320, anchor=W, font=("Purisa",10), text="Neftçala = 185", fill = "white")
w.create_text(850,340, anchor=W, font=("Purisa",10), text="Əli-bayramlı(Şirvan) = 135", fill = "white")
w.create_text(850,360, anchor=W, font=("Purisa",10), text="Yardımlı = 292", fill = "white")
w.create_text(850,380, anchor=W, font=("Purisa",10), text="Masallı = 236", fill = "white")
w.create_text(850,400, anchor=W, font=("Purisa",10), text="Lerik = 329", fill = "white")
w.create_text(850,420, anchor=W, font=("Purisa",10), text="Astara = 317", fill = "white")
w.create_text(850,440, anchor=W, font=("Purisa",10), text="Lənkaran = 272", fill = "white")
w.create_text(850,460, anchor=W, font=("Purisa",10), text="Balakən = 441", fill = "white")
w.create_text(850,480, anchor=W, font=("Purisa",10), text="Zaqatala = 318", fill = "white")
w.create_text(850,500, anchor=W, font=("Purisa",10), text="Qax = 402", fill = "white")
w.create_text(850,520, anchor=W, font=("Purisa",10), text="Şəki = 352", fill = "white")
w.create_text(850,540, anchor=W, font=("Purisa",10), text="Oğuz = 348", fill = "white")
w.create_text(850,560, anchor=W, font=("Purisa",10), text="Ağdam = 145", fill = "white")
w.create_text(850,580, anchor=W, font=("Purisa",10), text="Kəlbəcər = 160", fill = "white")
w.create_text(850,600, anchor=W, font=("Purisa",10), text="Laçın = 165", fill = "white")
w.create_text(850,620, anchor=W, font=("Purisa",10), text="Xocalı = 160", fill = "white")
w.create_text(850,640, anchor=W, font=("Purisa",10), text="Xocavənd = 155", fill = "white")
w.create_text(850,660, anchor=W, font=("Purisa",10), text="Fizuli = 145", fill = "white")
w.create_text(850,680, anchor=W, font=("Purisa",10), text="Zəngilan = 140", fill = "white")
w.create_text(850,700, anchor=W, font=("Purisa",10), text="Qusar = 182", fill = "white")
w.create_text(850,720, anchor=W, font=("Purisa",10), text="Quba = 168", fill = "white")
w.create_text(1000,220, anchor=W, font=("Purisa",10), text="Xaçmaz = 161", fill = "white")
w.create_text(1000,240, anchor=W, font=("Purisa",10), text="Siyəzən = 105", fill = "white")
w.create_text(1000,260, anchor=W, font=("Purisa",10), text="Xızı = 101", fill = "white")
w.create_text(1000,280, anchor=W, font=("Purisa",10), text="Xırdalan = 16", fill = "white")
w.create_text(1000,300, anchor=W, font=("Purisa",10), text="Sumqayıt = 39", fill = "white")
w.create_text(1000,320, anchor=W, font=("Purisa",10), text="Bakı = 0", fill = "white")


res = []
def printfunction():
    global res
    for r in res:
        r.destroy()
    res=[]
    try:
        Inputforfirstregion = Entryforfirstregion.get()
        Inputforlastregion = Entryforlastregion.get()
    except:

        LabelError = Label(w, text = 'Enter both regions!')
        LabelError.pack()
        w.create_window(650, 170, window = LabelError)



    umumi_cost = graph.Astarfunksiyasi(Inputforfirstregion, Inputforlastregion) # executes the algorithm

    if Inputforfirstregion=="Balakan" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeBalakan, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Agstafa" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeAgstafa, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Qabala" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeQabala, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Qazax" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeQazax, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Tovuz" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeTovuz, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Shamkir" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeShamkir, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Ganja" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeGanja, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Yevlax" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(Yevlax, nodeBaku) # executes the algorithm
    elif Inputforfirstregion=="Aghdash" and Inputforlastregion == "Baku":
        umumi_cost = graph.Astarfunksiyasi(nodeAgdash, nodeBaku) # executes the algorithm

    #Statements for Astar functions
    #if Inputforfirstregion == "" and Inputforlastregion == """
        #umumi_cost = graph.Astarfunksiyasi(node, node)

    path=''
    path = graph.yoluTap() # gets path
    result = ('Graph-ın ümumi costu: %s kilometrdir. Yol: %s ' % (umumi_cost, ' -> '.join(path)))

    #res.append(LabelforResult)
    if umumi_cost:
        LabelforResult = Label(w, text = result)
        LabelforResult.pack()
        w.create_window(650, 70, window = LabelforResult)
        res.append(LabelforResult)
        #print(result)
    else:
        LabelNotResult = Label(w, text = "Nəticə tapılmadı!")
        LabelNotResult.pack()
        w.create_window(650,70, window = LabelNotResult)
        print('Nəticə tapılmadı!')



widget1 = Label(w, text='İlk şəhəri əlavə edin!', fg='white', bg='black')
widget1.pack()
w.create_window(500, 100, window=widget1)

widget2 = Label(w, text='Sonuncu şəhəri əlavə edin!', fg='white', bg='black')
widget2.pack()
w.create_window(500,140, window = widget2)

Entryforfirstregion = Entry(w)
Entryforfirstregion.pack()
w.create_window(650,100, window = Entryforfirstregion)

Entryforlastregion = Entry(w)
Entryforlastregion.pack()
w.create_window(650,140, window = Entryforlastregion)


ButtonforfindingAstar = Button(w, text = "Axtarışa ver!", command = printfunction)
ButtonforfindingAstar.pack()
w.create_window(800,120, window = ButtonforfindingAstar)



#printfunction()


master.mainloop()
