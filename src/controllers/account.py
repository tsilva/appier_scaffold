#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import models

class AccountController(appier.Controller):

    @appier.route("/accounts.json", "GET")
    @appier.ensure(token = "base")
    def list(self):
        accounts = models.Account.find()
        return accounts
