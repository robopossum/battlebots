#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 19:58:32 2019

@author: tom
"""
from datetime import datetime as dt
import pandas as pd
import splinter
import random
import json
import time
from threading import Thread

class browserEnvironment():
    currentAction = str()
    def resetEnvironment(self):
        if self.browser is not None:
            self.browser.quit()
        browser = splinter.Browser()
        time.sleep(5)
        browser.visit("http://localhost:3000")
        time.sleep(5)
        self.browser = browser

    def __init__(self):
        self.browser = None
        self.resetEnvironment()

    def getState(self):
        return self.browser.evaluate_script("clientState")

    def takeAction(self, actions):
        jsCommand = str()
        for k,v in actions.items():
            if k in ['agentId', 'messageType']:
                continue
            jsCommand = "clientControl.{} = {};".format(k,v)
            self.browser.evaluate_script(jsCommand)
        #time.sleep(0.2)


    # def getScore

# test scripts
if __name__ == "__main__":
    print("hEllo")
    # we first start the browser
    brow = browserEnvironment()

    # then we confirm we can access a state;
    state = brow.getState()

    # state should be dict as;
"""
{'agentId': 1,
 'canShoot': True,
 'dX': 0,
 'dY': 0,
 'messageType': 'frame',
 'sensors': [{'angle': -50, 'hitting': 0, 'length': 125},
  {'angle': -45, 'hitting': 0, 'length': 125},
  {'angle': -40, 'hitting': 0, 'length': 125},
  {'angle': -35, 'hitting': 0, 'length': 125},
  {'angle': -30, 'hitting': 0, 'length': 125},
  {'angle': -25, 'hitting': 0, 'length': 125},
  {'angle': -20, 'hitting': 0, 'length': 125},
  {'angle': -15, 'hitting': 0, 'length': 125},
  {'angle': -10, 'hitting': 0, 'length': 125},
  {'angle': -5, 'hitting': 0, 'length': 125},
  {'angle': 0, 'hitting': 0, 'length': 125},
  {'angle': 5, 'hitting': 0, 'length': 125},
  {'angle': 10, 'hitting': 0, 'length': 125},
  {'angle': 15, 'hitting': 0, 'length': 125},
  {'angle': 20, 'hitting': 0, 'length': 125},
  {'angle': 25, 'hitting': 0, 'length': 125},
  {'angle': 30, 'hitting': 0, 'length': 125},
  {'angle': 35, 'hitting': 0, 'length': 125},
  {'angle': 40, 'hitting': 0, 'length': 125},
  {'angle': 45, 'hitting': 0, 'length': 125},
  {'angle': 50, 'hitting': 0, 'length': 125}],
 'x': 400,
 'xp': 0,
 'y': 300}
"""