import numpy as nump
from numpy import *
import matplotlib.pyplot as graph  #matlab versiyasi pythonun
import pandas #csv faylini read etmek ucun

numberofiterations = 1500
learningrate = 0.01

def plot(population, profit):
    graph.plot(population, profit,'.', markersize=7, color = "red")
    graph.xlabel('Şəhərdəki əhalinin sayı')
    graph.ylabel('Şəhərdəki kamaz xeyri')
    #graph.show(block = True)
    #graph.close()

def datatobeTaken():
    data = genfromtxt("ex1data1.txt", delimiter=",") #delimiter used to seperate values with ,
    #data = pandas.read_csv("data.csv")
    #data = nump.loadtxt("data.txt", delimiter = ",")

    population = data[:, 0] #x axis of data
    profit = data[:, 1] # y axis of data
    m = len(profit) #m is the number of instances
    profit = profit.reshape(m,1) #output instances for profit or y which is output
    return population, profit; # returns x and y

def datatobePlotted():
    population, profit = datatobeTaken(); #x and y should be get from data file
    plot(population, profit) # then adding those datas into the plot
    graph.show(block=True) #showing in the graph

#updateruleient Descent Loop

def hfunction(population, theta):
    return population.dot(theta)

#Cost function to be computed by using variables
def costFunctiontobeComputed(population, profit, theta):
    m = len(profit) #m is the instances of y or profit
    sumofvariables = 0 #cost function is equal to 0 from beginning
    for i in range(1, m): #where i starts from 1 till m which is the lenght of profit
        sumofvariables += (hfunction(population[i],theta) - profit[i])**2 #cost function from 1 to m
    sumofvariables = sumofvariables * (1.0/(2*m))  #cost function for the linear regression


    return sumofvariables

def costnumber2(population, profit, theta):
    m = len(profit) #m is the instances of y or profit
    sumofvariables = 0 #cost function is equal to 0 from beginning
    for i in range(1, m): #where i starts from 1 till m which is the lenght of profit
        sumofvariables += (hfunction(population[i],theta) - profit[i]) #cost function from 1 to m
    sumofvariables = sumofvariables * (1.0/(m))  #cost function for the linear regression


    return sumofvariables

#Update rule to be computed
def updateruletobeComputed(population, profit, theta, learningrate, numberofiterations):
    #Compute Oj = Oj - learningrate*costFunctiontobeComputed

    m = len(profit) #m is the instances of y or profit
    k=theta[0]
#for izzz in range(0,len(theta)):
    #theta[izzz] = theta[izzz] - learningrate * costnumber2(population, profit, theta)
    theta[0] = theta[0] - learningrate * costnumber2(population, profit, theta)
    theta[1] = theta[1] - learningrate * costnumber2(population, profit, theta)

    #theta[2] = theta[2] - learningrate * costnumber2(population, profit, theta)
    #theta[k] = theta[k] - learningrate * costnumber2(population, profit, theta)
    for i in theta:
        print(i)

    return theta

def tobePrinted():

    numberofiterations = 1500 #no. of interations to learn
    learningrate = 0.01 #learning rate is 0.01

    population, profit = datatobeTaken();
    m = len(profit) #m is the instances of y or profit
    population = c_[ones((m, 1)),population] #add theta zero coloumn to obstruct c_ for aligning

    theta = [0,0] #used as vector in order to show theta one and theta zero
    for i in range(0,numberofiterations):
        costfinished = costFunctiontobeComputed(population, profit, theta) #getting cost from cost function
        theta = updateruletobeComputed(population, profit, theta, learningrate, numberofiterations) #getting theta from update rule
        print("Cost function in iteration '%d' '%d': ",i, costfinished)
        print(theta[0],theta[1])

    #theta = updateruletobeComputed(population, profit, theta, learningrate, numberofiterations) #getting theta from update rule
    print("The cost function is:", costfinished) #printing cost
    #print("The theta in 1500s iterations is:", theta[0], theta[1]) #printing theta zero and theta one

    plot(population[:, 1], profit[:,0]) #adding the dots inside the graph
    graph.plot(population[:, 1],population.dot(theta)) #adding the line for the theta into the graph
    graph.show(block=True) #showing the graph itself
    graph.close() #closing the graph

#Printing the plot
tobePrinted()
#Reference
#https://matplotlib.org/tutorials/introductory/pyplot.html
