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

templateControlObject = {
            "agentId": 1,
            "messageType": "control",
            "up": 0,
            "down": 0,
            "left": 0,
            "right": 0,
            "mouseX": 0,
            "mouseY": 0,
            "click": 0,
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
            "mouseX": 0,
            "mouseY": 0,
            "click": 0,
            }

    def setState(self, state):
        self.state = state

    @DefFacts()
    def _init__(self):
        yield Fact(action='waking')

# rule 1
    @Rule(Fact(action='explore'))
    def makeRandomMove(self):
        self.chainOfLogic.append("Because I am exploring, I look around")
        self.controlObject = templateControlObject.copy()
        choice = (random.choice(['up', 'down', 'left', 'right']))
        print("Choice is ", choice)
        self.controlObject[choice] = 1





import random

# states
        # explore
        # exploit
        # fight
        # flee





bot = aiBumbleFuckAgent()
bot.duplicate = True

import time


while True:
    bot.reset()
    bot.declare(Fact(action='explore'))
    bot.run()
    for k,v in bot.controlObject.items():
        if k in ['agentId', 'messageType']:
            continue
        browser.evaluate_script("clientControl.{} = {}".format(k,v))
    time.sleep(1)


