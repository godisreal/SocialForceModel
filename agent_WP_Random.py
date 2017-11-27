# -*-coding:utf-8-*-
# Author: Shen Shen and Wang Peng
# Email: dslwz2002@163.com

import numpy as np
from tools import *
import random

class Agent(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        
        self.posX = random.uniform(8,24)
        self.posY = random.uniform(8,18)
        self.pos = np.array([self.posX, self.posY])
        #self.pos = np.array([10.0, 10.0])

        self.actualVX = 0 #random.uniform(0,1.6)
        self.actualVY = 0 #random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX, self.actualVY])
        #self.actualV = np.array([0.0, 0.0])

        self.dest = np.array([60.0,10.0])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])
        
        self.desiredSpeed = 1.8 #random.uniform(0.3,2.3) #1.8
        self.desiredV = self.desiredSpeed*self.direction
        
        self.acclTime = random.uniform(8,16) #10.0
        self.drivenAcc =(self.desiredV - self.actualV)/self.acclTime
               
        self.mass = 60 #random.uniform(40,90) #60.0
        self.radius = 0.35 #1.6 
        self.interactionRange = 3
        self.p = 0.6
        
        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = 1
        self.B = 0.8 #random.uniform(0.8,1.6) #0.8 #0.08
        
	self.Goal = 0
	self.timeOut = 0.0
	
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
        

    # def step(self):
    #     # 初始速度和位置
    #     v0 = self.actualV
    #     r0 = self.pos
    #     self.direction = normalize(self.dest - self.pos)
    #     # 计算受力
    #     adapt = self.adaptVel()
    #     peopleInter = self.peopleInteraction()
    #     wallInter = self.wallInteraction()
    #     sumForce = adapt + peopleInter + wallInter
    #     # 计算加速度
    #     accl = sumForce/self.mass
    #     # 计算速度
    #     self.actualV = v0 + accl # consider dt = 1
    #     # 计算位移
    #     self.pos = r0 + v0 + 0.5*accl
    #     print(accl,self.actualV,self.pos)

        
        
    def adaptVel(self):
        deltaV = self.desiredV - self.actualV
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.acclTime


    def attr(self, xx, yx): #, Vx=1, Vy=1):
	self.posX = xx
        self.posY = yx
        self.pos = np.array([self.posX, self.posY])
        #self.actualVX = Vx
        #self.actualVY = Vy
        #self.actualV = np.array([self.actualVX, self.actualVY])
        return
        

    def peopleInteraction(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        # rij = desiredDistance(selfID, otherID)
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = Afactor*self.A*np.exp((rij*Dfactor-dij)/(self.B*Bfactor))*nij*20
        + self.bodyFactor*g(rij-dij)*nij*1000000  #/10000
        #tij = np.array([-nij[1],nij[0]])
        #deltaVij = (self.actualV - other.actualV)*tij
        #second = self.slideFricFactor*g(rij-dij)*deltaVij*tij
        return first #+ second

    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = -self.A*np.exp((ri-diw)/self.B)*niw*160
        + self.bodyFactor*g(ri-diw)*niw/10000
        #tiw = np.array([-niw[1],niw[0]])
        #second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw
        return first #- second

    #def wallOnRoute(self, wall):
	#self.pos
	#self.actualV
	#return true
		
		
    #def peopleInterDV(self, other):
	#rij = self.radius + other.radius
        #dij = np.linalg.norm(self.pos - other.pos)
        #nij = (self.pos - other.pos)/dij
        
        #if dij < self.interactionRange:
	#    self.desiredV = self.p*self.desiredV + #(1-self.p)*other.desiredV			
        #return dij
        
        
