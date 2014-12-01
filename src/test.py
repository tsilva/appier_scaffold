#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import scheduler

class HelloApp(appier.App):

    def __init__(self):
        appier.App.__init__(self)
        self.scheduler = scheduler.Scheduler(self)

    def start(self):
        appier.App.start(self)
        self.scheduler.start()

HelloApp().serve()
