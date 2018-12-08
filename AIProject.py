# encoding:utf-8

import heapq as hpg # queue uchun
from collections import defaultdict # listleri gostermek uchun
from tkinter import *
import tkinter

#Stackdaki elemetleri gosteren class
class Stackadielementler:

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

                queue = Stackadielementler() # queue duzeldir

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
nodeAghdam = Node('Aghdam', 145)
nodeKalbacar = Node('Kalbacar', 160)
nodeLachin = Node('Lachin', 165)
nodeXocali = Node('Xocali', 160)
nodeXocavend = Node('Xocavend', 155)
nodeFizuli = Node('Fizuli', 145)
nodeZangilan = Node('Zangilan', 140)

nodeQusar = Node('Qusar', 30)
nodeQuba = Node('Quba', 30)
nodeXachmaz = Node('Xachmaz', 30)
nodeSiyezen = Node('Siyezen', 30)
nodeXizi = Node('Xizi', 30)

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

w = Canvas(master, width=800, height=600,bd=0,highlightthickness=0)

w.configure(bg="black")
w.pack()

w.create_line(20,200, 40, 100, fill = "white", width = 2) #nodeAgstafa
w.create_text(35, 90, anchor=W, font=("Purisa",10), text="Agstafa", fill = "white")
w.create_text(20, 195, anchor=W, font=("Purisa",10), text="Qazax", fill = "white")

w.create_line(40,100, 80, 200, fill = "white", width = 2) #Tovuz
w.create_text(75, 185, anchor=W, font=("Purisa",10), text="Tovuz", fill = "white")

w.create_line(80,200, 130, 190, fill = "white", width = 2) #Shamkir
w.create_text(130, 185, anchor=W, font=("Purisa",10), text="Shamkir", fill = "white")

w.create_line(130,190, 160, 210, fill = "white", width = 2) #ganja
w.create_text(160, 205, anchor=W, font=("Purisa",10), text="Ganja", fill = "white")

w.create_line(160,210, 110 , 300, fill = "white", width = 2) #Kalbacar
w.create_text(110, 305, anchor=W, font=("Purisa",10), text="Kalbacar", fill = "white")

w.create_line(160,210, 180, 250, fill = "white",width = 2) #Tartar
w.create_text(180, 255, anchor=W, font=("Purisa",10), text="Tartar", fill = "white")

w.create_line(180,250, 200, 260, fill = "white", width = 2) #Tartar-Barda
w.create_text(200, 265, anchor=W, font=("Purisa",10), text="Barda", fill = "white")

w.create_line(160,210, 190, 210, fill = "white", width = 2) #Yevlax
w.create_text(190, 205, anchor=W, font=("Purisa",10), text="Yevlax", fill = "white")

w.create_line(190,210, 200, 260, fill = "white", width = 2) #Barda
w.create_text(200, 255, anchor=W, font=("Purisa",10), text="Barda", fill = "white")

w.create_line(200,260, 190, 330, fill = "white", width = 2) #Barda - Agdam
w.create_text(190, 325, anchor=W, font=("Purisa",10), text="Agdam", fill = "white")

w.create_line(190,210, 210, 230, fill = "white", width = 2) #Agdash
w.create_text(210, 225, anchor=W, font=("Purisa",10), text="Aghdash", fill = "white")

w.create_line(110, 300, 120, 350, fill = "white", width = 2) #Lacin
w.create_text(120, 345, anchor=W, font=("Purisa",10), text="Lacin", fill = "white")

w.create_line(120,350, 160, 350, fill = "white", width = 2) #Xocali
w.create_text(160, 345, anchor=W, font=("Purisa",10), text="Xocali", fill = "white")

w.create_line(160,350, 190, 330, fill = "white", width = 2) #Aghdam

w.create_line(190, 330, 210, 360, fill = "white", width = 2) #nodeXocavend
w.create_text(210, 355, anchor=W, font=("Purisa",10), text="Xocavend", fill = "white")

w.create_line(210,360, 230, 380, fill = "white", width = 2) #Fizuli
w.create_text(230, 375, anchor=W, font=("Purisa",10), text="Fizuli", fill = "white")

w.create_line(230, 380, 220, 430, fill = "white", width = 2) #Zangilan
w.create_text(220, 425, anchor=W, font=("Purisa",10), text="Zangilan", fill = "white")

w.create_line(220,430, 270, 370, fill = "white", width = 2) #Imishli
w.create_text(270, 365, anchor=W, font=("Purisa",10), text="Imishli", fill = "white")

w.create_line(270,370, 230, 380, fill = "white", width = 2) #Imishli-nodeFizuli

w.create_line(270,370, 280, 320, fill = "white", width = 2) #Imisli - Kurdamir
w.create_text(280, 315, anchor=W, font=("Purisa",10), text="Kurdamir", fill = "white")

w.create_line(280,320, 245, 305, fill = "white", width = 2) #Kurdamir - Zardab
w.create_text(245, 300, anchor=W, font=("Purisa",10), text="Zardab", fill = "white")

w.create_line(280,320, 230, 260, fill = "white", width = 2) #Kurdamir-Ucar
w.create_text(230, 255, anchor=W, font=("Purisa",10), text="Ucar", fill = "white")

w.create_line(245,305, 230, 260, fill = "white", width = 2) #Zardab - Ucar

w.create_line(230,260, 240, 220, fill = "white", width = 2) #Ucar - Goycay
w.create_text(240, 215, anchor=W, font=("Purisa",10), text="Goycay", fill = "white")

w.create_line(240,220, 210, 230, fill = "white", width = 2) # Goycay-Agdash
w.create_text(210, 225, anchor=W, font=("Purisa",10), text="Agdash", fill = "white")

w.create_line(210,230, 250, 210, fill = "white", width = 2) #Agdash-nodeQabala
w.create_text(250, 205, anchor=W, font=("Purisa",10), text="Qabala", fill = "white")

w.create_line(250,210, 230, 180, fill = "white", width = 2) #Qabala-Oguz
w.create_text(230, 175, anchor=W, font=("Purisa",10), text="Oghuz", fill = "white")

w.create_line(230,180, 200, 170, fill = "white", width = 2) #Oguz-Seki
w.create_text(200, 165, anchor=W, font=("Purisa",10), text="Sheki", fill = "white")

w.create_line(200,170, 160, 140, fill = "white", width = 2) #Seki- Qax
w.create_text(160, 135, anchor=W, font=("Purisa",10), text="Qax", fill = "white")

w.create_line(160,140, 150, 120, fill = "white", width = 2) #Qax-Zaqatala
w.create_text(150, 115, anchor=W, font=("Purisa",10), text="Zaqatala", fill = "white")

w.create_line(150,120, 120, 60, fill = "white", width = 2) #Zaqatala-Balakan
w.create_text(120, 55, anchor=W, font=("Purisa",10), text="Balakan", fill = "white")


#Naxcivan
w.create_line(30,290, 60, 370, fill = "white", width = 2) #Sadarak - Sarur
w.create_text(30, 285, anchor=W, font=("Purisa",10), text="Sadarak", fill = "white")
w.create_text(60, 365, anchor=W, font=("Purisa",10), text="Sharur", fill = "white")

w.create_line(60,370, 80, 390, fill = "white", width = 2) #Sarur Babak
w.create_text(80, 386, anchor=W, font=("Purisa",10), text="Babak", fill = "white")

w.create_line(80,390, 120, 370, fill = "white", width = 2) #Babak-Shahbuz
w.create_text(120, 365, anchor=W, font=("Purisa",10), text="Shahbuz", fill = "white")

w.create_line(80,390, 100, 430, fill = "white", width = 2) #Babak-nodeCulfa
w.create_text(100, 425, anchor=W, font=("Purisa",10), text="Culfa", fill = "white")

w.create_line(100,430, 160, 480, fill = "white", width = 2) #Culfa-Ordubad
w.create_text(160, 475, anchor=W, font=("Purisa",10), text="Ordubad", fill = "white")


def printfunction():

    umumi_cost = graph.Astarfunksiyasi(nodeBalakan, nodeBaku) # executes the algorithm
    path = graph.yoluTap() # gets path
    result = ('Graph-ın ümumi costu: %s kilometrdir. Yol: %s ' % (umumi_cost, ' -> '.join(path)))

    if umumi_cost:
        print(result)
    else:

        print('Nəticə tapılmadı!')

printfunction()

master.mainloop()
