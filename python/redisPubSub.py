#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:58:32 2019

@author: tom
"""

# import redis
# listener = redis.Redis(port=2341)
# pubsub = listener.pubsub()
# pubsub.subscribe("Sick beats yooo")
# pubsub.get_message()

from pyknow import Fact, Rule, KnowledgeEngine, DefFacts, AND, NOT, W, TEST, MATCH, OR
import splinter
browser = splinter.Browser()
browser.visit("http://localhost:3000")
import json
import random
import pandas as pd

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

class aiBumbleFuckAgent(KnowledgeEngine):
    chainOfLogic = list()
    controlObject = {
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

    def setState(self, state):
        self.state = state
        self.checkSensorExp()

    @DefFacts()
    def _init__(self):
        yield Fact(action='waking')

# rule 1
    @Rule('action' << Fact(action='explore'),
          )
    def makeRandomMove(self, action):
        #print("Making Random Move")
        self.chainOfLogic.append("Because I am exploring, I look around")
        self.controlObject = templateControlObject.copy()
        avoidWall = self.checkSensorWall()
        if avoidWall is not None:
            self.controlObject[avoidWall] = 1
        choice = (random.choice(['up', 'left', 'right', 'turnLeft', 'turnRight']))
#        print("Choice is ", choice)
        self.controlObject[choice] = 1

        if random.randint(0,1):
            self.controlObject['shoot'] = 1

        self.declare(Fact(action='pendingUpdate'))
        #print("TRying toretract", action)
        self.retract(action)


    def checkSensorWall(self):
        stateDf = pd.DataFrame.from_records(self.state['sensors'])
        leftSens = (stateDf[stateDf['angle'] < 0 ][stateDf['hitting'] == 4]).shape[0]
        rightSens = (stateDf[stateDf['angle'] > 0 ][stateDf['hitting'] == 4]).shape[0]
        self.stateDf = stateDf
        if leftSens > rightSens:
            #print("Turn Right!")
            # turn right
            return 'right'
        elif leftSens < rightSens:
           # print("Turn Left!")

            # turn left
            return 'left'
        else:
            return None

    def checkSensorExp(self):
        stateDf = pd.DataFrame.from_records(self.state['sensors'])
        if stateDf[stateDf['hitting'] == 2].empty:
            self.declare(Fact(action='explore'))

            print("Exploring!!!", dt.now().isoformat())

        else:
            self.declare(Fact(action='exploit'))
            print("Exploiting!!MAKE STOP !!", dt.now().isoformat())


    @Rule('fact' << Fact(action='exploit'),
          salience = 1)
    def navigateToExp(self, fact):
        #print("Exploiting method in !!!")
        #pprint.pprint(self.state)
        #input("Press any to continue")
        def getMove(self):
            stateDf = pd.DataFrame.from_records(self.state['sensors'])
            leftSens = (stateDf[stateDf['angle'] < -10 ][stateDf['hitting'] == 2]).shape[0]
            rightSens = (stateDf[stateDf['angle'] > 10 ][stateDf['hitting'] == 2]).shape[0]
            self.stateDf = stateDf
            if not (stateDf[stateDf['angle'] <= 10 ][stateDf['hitting'] == 2][stateDf['angle'] >= -10]).empty:
                print("go forwards")
                return 'up'
            elif leftSens > rightSens:
                print("Turn Left!")
                return 'left'
            elif leftSens < rightSens:
                print("Turn right!")
                return 'right'


        self.controlObject['down'] = 0
        self.controlObject['left'] = 0
        self.controlObject['right'] = 0
        self.controlObject[getMove(self)] = 1
        self.retract(fact)
# states
        # explore
        # exploit
        # fight
        # flee


from datetime import datetime as dt




bot = aiBumbleFuckAgent()
bot.reset()
bot.duplicate = True
bot.declare(Fact(action='explore'))

import time
import pprint

while True:

    bot.setState(browser.evaluate_script("clientState"))
    bot.run()
    for k,v in bot.controlObject.items():
        if k in ['agentId', 'messageType']:
            continue
        browser.evaluate_script("clientControl.{} = {}".format(k,v))
    time.sleep(1/100)

