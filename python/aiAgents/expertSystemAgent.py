#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:32:52 2019

@author: tom
"""
from pyknow import *
import pandas as pd
from datetime import datetime as dt
import random
templateControlObject = {
            "agentId": 1,
            "messageType": "control",
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
            "turnLeft": 0,
            "turnRight": 0,
            "shoot": 0,
            }


class expertSystemBasedAgent(KnowledgeEngine):
    chainOfLogic = list()
    controlObject = dict()

    def setState(self, state):
        self.reset()
        self.state = pd.DataFrame.from_records(state['sensors'])
        self.declare(Fact(action='sensing'))
        self.run()

    def getAction(self):
        return self.controlObject

    @DefFacts()
    def _init__(self):
        yield Fact(action='sensing')

    # rule 1
    @Rule('action' << Fact(action='sensing'))
    def checkOurSensors(self, action):
        df = self.state
 #       print("Checking Sensors :", dt.now().isoformat())
        # TODO we need to check if we are hitting food, an enemy, walls or exp
        # we see if we can see anything at all
        self.declare(Fact(seeNothing=((len(df[df['hitting']==0]) == 21))))

        # we see if we can see exp;
        self.declare(Fact(seeExp=((len(df[df['hitting']==2]) != 0))))

        # we see if we can see a wall;
        self.declare(Fact(seeWall=((len(df[df['hitting']==4]) != 0))))


        self.retract(action)



    # rule 2
    @Rule('action' << Fact(seeExp=True))
    def seeExp(self, action):
        # we should have more logic in here , howevr for now..
        self.declare(Fact(action='exploit'))
        self.retract(action)

#


    # rule 3
    @Rule('action' << Fact(seeNothing=True))
    def makeRandomMove(self, action):
        #print("Making Random Explore move")
        self.controlObject = templateControlObject.copy()
        choice = (random.choice(['up', 'up', 'up', 'up', 'up', 'up', 'turnLeft', 'turnRight']))
        self.controlObject[choice] = 1
        self.retract(action)


    # rule 3
    @Rule('action' << Fact(seeWall=True))
    def avoidWall(self, action):
        #print("Avoiding Walls!")
        df = self.state
        lSens = sum(df[(df['hitting'] == 4) & (df['angle'] < 0)]['length'])
        rSens = sum(df[(df['hitting'] == 4) & (df['angle'] > 0)]['length'])
        self.controlObject = templateControlObject.copy()
        if lSens < rSens:
        #    print("tunring left")
            self.controlObject['turnLeft'] = 1
            self.controlObject['down'] = 1
        if lSens > rSens:
         #   print("tunring right")
            self.controlObject['turnRight'] = 1
            self.controlObject['down'] = 1
        self.retract(action)



    @Rule('fact' << Fact(action='exploit'),
          salience = 1)
    def navigateToExp(self, fact):
        def getMove(self):
            df =self.state
            targets = df[df['hitting'] == 2].sort_values('length',
                                                         ascending=False)
            nearest = targets.iloc[0]
            if nearest.angle >=-6 and nearest.angle <= 6:
                self.controlObject['up'] = 1
            elif nearest.angle < -6:
#                self.controlObject['left'] = 1
                self.controlObject['turnLeft'] = 1
            elif nearest.angle > 6:
#                self.controlObject['right'] = 1
                self.controlObject['turnRight'] = 1
            #return 'up'
        self.controlObject = templateControlObject.copy()
        self.controlObject['up'] = 1
        # self.controlObject['down'] = 0
        # self.controlObject['left'] = 0
        # self.controlObject['right'] = 0
        # print(getMove(self))
        #self.controlObject[getMove(self)] = 1
        getMove(self)
        self.retract(fact)
