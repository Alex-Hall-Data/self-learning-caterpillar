# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 17:16:22 2016

@author: Alex
"""
import matplotlib.pyplot as plt
import matplotlib
from math import tan,asin
import random
import time
import copy
import numpy as np

#parameters for genetic algorithm
####################################################
#NUMBER OF MOVES PER SEQUENCE
nomoves=100
#population size
popsize=100
#caterpillarsize
catsize=10
##########################################################

#class to create segment objects
class segment(object):
    def __init__(self,positionx,positiony):
        self.positionx=positionx
        self.positiony=positiony
        
    #establish position of segnemt and plot
    def plotsegment(self,positionx,positiony):
        segment=plt.Circle((positionx,positiony),.2,color='r')
        fig = plt.gcf()
        axes=plt.gca()
        axes.set_xlim([0,20])
        axes.set_ylim([0,8])
        fig.gca().add_artist(segment)
    

    #method to raise the segment. if raise=1, raise the segment by 0.02
def raisesegment(segment,up):
    
    positiony=segment.positiony
    #positionx=segment.positionx
        #if we are rasinig the segment        
    if up==1:
            #check y pososition has not exceeded maximum
       # if positiony<1.2:##needs changing - 1.2 isn't an absolute max
        positiony+=0.02
     #   else:
      #      positiony=positiony
                
    if up==0:
        positiony=positiony
            
    if up==-1:
        if positiony<=1:
            positiony=positiony
        else:
            positiony-=0.02
                
    return positiony
 ########################################## CHANGE CALUES WITH DIFFERENT CATERPILLAR LENGTH
#initiate a caterpillar
segment1=segment(10,1.0)
segment2=segment(10.4,1.0)
segment3=segment(10.8,1.0)
segment4=segment(11.2,1.0)
segment5=segment(11.6,1.0)
segment6=segment(12.0,1.0)
segment7=segment(12.4,1.0)
segment8=segment(12.8,1.0)
segment9=segment(13.2,1.0)
segment10=segment(13.6,1.0)
segmentlist=[segment1,segment2,segment3,segment4,segment5,segment6,segment7,segment8,segment9,segment10]
startsegmentlist=[segment(10,1.0),segment(10.4,1.0),segment(10.8,1.0),segment(11.2,1.0),segment(11.6,1.0),segment(12.0,1.0),segment(12.4,1.0),segment(12.8,1.0),segment(13.2,1.0),segment(13.6,1.0)]
possiblepivotnumbers=[0,1,2,3,4,5,6,7,8,9]#needs changing for a larger caterpillar
maxheights=[1.0,1.2,1.4,1.6,1.8,1.8,1.6,1.4,1.2,1.0] #max height of each  segment (should really make this automatic)


#This section gives an initial population in the following format: [[caterpillar[move[[segment,lock]]]],[],[]...]
##################################################

possibleraise=[-1,0,1]
pivot=0 
#possiblepivots=list()
initialmoves=[]
initialupdownlist=[]
initialpopmoveslist=[[] for _ in range(popsize)]

#get a list of initial up/downs
def initialupdown(initialupdownlist,nomoves,startsegmentlist,possibleraise):
    initialupdownlist=[]
    for i in range(0,nomoves):
        initialupdownlist.append([])
        for j in range(1,len(startsegmentlist)-1):
            initialupdownlist[i].append(random.choice(possibleraise))
    return initialupdownlist

#initial list of moves for a caterpillar
def caterpillarmoveslist(nomoves,initialmoves,initialupdownlist,possiblepivotnumbers):
    initialmoves=[]
    for i in range(0,nomoves):
        initialmoves.append([initialupdownlist[i],[random.choice(possiblepivotnumbers)]])
    return initialmoves
    
popmoves=[]
#get initial moves for all of the initial population - CALL THIS TO CREATE AN INITIAL POPULATION
def initialpopmoves(popsize):
        
        for p in range(popsize):
                popmoves.append(caterpillarmoveslist(nomoves,initialmoves,initialupdown(initialupdownlist,nomoves,startsegmentlist,possibleraise),possiblepivotnumbers))
        #return initialpopmoveslist
    
population=popmoves
#####################################


#build a single caterpillar from the segment objects-TAKES one item (ie, caterpillar) from popmoves as an input
#returns a list in the form [move[segment[xpos,ypos]]]
def buildcaterpillar(moveslist):#sg list is initial segmentlist for first iteration and successive segmentlists for next iterations
    fullist=[]#list of all segments for each move
    #list of segment objects
    sglist=copy.deepcopy(startsegmentlist) 
    #for each move
    for k in range(len(moveslist)):
        #for each segment     
        for i in range(len(moveslist[k][0])):
        
        
        #change y positions according to moveslist
            sglist[i+1].positiony=raisesegment(sglist[i+1],moveslist[k][0][i])
                       
            #ensure doesnt exceed maximum
            if sglist[i+1].positiony-sglist[i].positiony>0.2:
                sglist[i+1].positiony=sglist[i].positiony+0.2
                #ensure doesnt exceed minimum   
            if sglist[i+1].positiony-sglist[i].positiony<-0.2:
                sglist[i+1].positiony=sglist[i].positiony-0.2
           
            if sglist[i+1].positiony>maxheights[i+1]:
                sglist[i+1].positiony=maxheights[i+1]
                
           
        ypos=[]
        for segment in sglist:
            ypos.append(segment.positiony)
                        #return ypos
    

        possiblepivots=[]
        #get list of possible pivot points
        for i in range(len(sglist)):
            if sglist[i].positiony ==1:
                 possiblepivots.append(i)
            #pivot = nearest to moveslist[k][1][0]
            differences=[]
            #list of differences between proposed and possible pivots
            for point in possiblepivots:
                difference=abs(point-moveslist[k][1][0])
                differences.append(difference)
            #index of possible pivot with minimum difference from proposed
            ind=differences.index(min(differences))
        #print(possiblepivots)
        
        #get index of pivot - 
        pivot=possiblepivots[ind]##
        #print(pivot)
        
        #generate x position of segments to the right of the highest one 
        for i in range(pivot+1,len(segmentlist)): 
            #height difference between segments
            h=sglist[i-1].positiony-sglist[i].positiony
            if h!=0:
                sglist[i].positionx=sglist[i-1].positionx+((h)/(tan(asin(h/0.4))))
            else:
                sglist[i].positionx=sglist[i-1].positionx+0.4
                 
            
 #      #generate x position of segments to the left of the highest one
        for i in range(pivot,0,-1):
            h=sglist[i].positiony-sglist[i-1].positiony
            if h!=0:
                sglist[i-1].positionx=sglist[i].positionx-((h)/(tan(asin(h/0.4))))
            else:
                sglist[i-1].positionx=sglist[i].positionx-0.4
        
    #return segmentlist[0].positionx
        #for segment in sglist:

            #print( segment.positiony)
        print(sglist[2].positiony)     
        #return list of coordinates
        fullist.append([[sglist[i].positionx,sglist[i].positiony] for i in range(len(sglist))])
    return fullist

positions=[0]*popsize#the list of positions (ie all the population). gives a list of segment objects which will be plotted later
result=[0]*popsize#list of foremost segment x position for each individual       

#create an initial population
initialpopmoves(popsize)

#evolves, using the current population list as input
#population is the thing we are evolving - need to output the next population
#currently this returns the result for a generation and a list of all the positions (to plot)
#takes the current population as the input (or initial population for the first iteration)
def iterate(pop):
    i=0
    for individual in pop:
        positions[i]=buildcaterpillar(individual)
        i+=1
        #positions.append(buildcaterpillar(individual))
    for index in range(popsize): #make list of finishing positions of form [x,y][x,y]...
        result[index]=positions[index][nomoves-1][catsize-1][0]
        
    
def evolve(pop,iterations,elite,):
    for i in range(iterations):
    #perform an evolution step        
        iterate(pop)
        #return indices of elite individuals
        winner_indices=np.argpartition(result,int(-elite*popsize)[(int(-elite*popsize)):]
        
        
    
   #plot the whole caterpillar - PROBABLY WON'T USE THIS SINCE WE ARE RETURNING COORDINATES NOW
#def plotcaterpillar(segmentlist):  
#    for item in segmentlist:
#        segment.plotsegment(item,item.positionx,item.positiony)
        
        
           