# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 17:43:00 2016

@author: Alex
"""
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation

filenametemplate=r'C:\Users\Alex\Documents\Python\genetic caterpillar\frames\cat{0:100}.png'
colist=['b','g','m','y','b','g','m','y','b','g']
def animatecaterpillar(movelist):
    fig = plt.figure(figsize=(12,10))
    ax=plt.axes(xlim=(8,20),ylim=(0,10))
    j=0
    for move in movelist[99]:#for move-CHANGE TO GET GENERATION
        col=0 #loop counter
        for i in movelist[99][j]:#for segment - CHANGE THIS TO SAME AS ABOVE
            
            circle=plt.Circle((i[0],i[1]),.2,color=colist[col])
            foot1=plt.Circle((i[0]+0.1,i[1]-0.25),.05,color=colist[col])
            foot2=plt.Circle((i[0]-0.1,i[1]-0.25),.05,color=colist[col])
            
            plt.gca().add_artist(circle)
            plt.gca().add_artist(foot1)
            plt.gca().add_artist(foot2)
            col+=1
        eye=plt.Circle((move[9][0]+0.12,move[9][1]+0.05),.03,color='k')
        antenna=plt.Circle((move[9][0]+0.12,move[9][1]+0.25),.03,color='g')
        smile=matplotlib.patches.Arc(xy=(move[9][0]+0.15,move[9][1]-0.05),width=0.2,height=0.1,angle=0,theta1=180,theta2=270)
        plt.gca().add_artist(smile)
        plt.gca().add_artist(antenna)
        plt.gca().add_artist(eye)
        j+=1
        plt.savefig(filenametemplate.format(j),format='png')
        plt.cla()