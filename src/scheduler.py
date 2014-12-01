#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

LOOP_TIMEOUT = 1800.0
""" The time value to be used to sleep the main sequence
loop between ticks, this value should not be too small
to spend many resources or to high to create a long set
of time between external interactions """

class Scheduler(appier.Scheduler):

    def __init__(self, *args, **kwargs):
        appier.Scheduler.__init__(
            self,
            timeout = LOOP_TIMEOUT,
            *args,
            **kwargs
        )

    def tick(self):
        appier.Scheduler.tick(self)
        self.logger.info("ticked")

    def load(self):
        appier.Scheduler.load(self)
        self.logger.info("loaded")
