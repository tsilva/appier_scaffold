#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import time
import uuid
import calendar
import datetime
import threading
import unidecode

import appier
import appier_extras

LOCKS_MAP = {}
""" Map with locks indexed by name """

class Base(appier_extras.admin.Base):

    id = dict(
        type = int,
        index = True,
        increment = True
    )

    unique_id = dict(
        index = True
    )

    enabled = dict(
        type = bool,
        index = True
    )

    create_date = dict(
        type = float,
        index = True
    )

    modify_date = dict(
        type = float,
        index = True
    )

    create_user = dict(
        type = appier.reference(
            "Account",
            name = "id"
        ),
        index = True
    )

    modify_user = dict(
        type = appier.reference(
            "Account",
            name = "id"
        ),
        index = True
    )

    description = dict(
        default = True
    )

    @classmethod
    def _build(cls, model, map):
        appier_extras.admin.Base._build(model, map)
        enabled = model.get("enabled", None)
        model["status"] = enabled and "enabled" or "disabled"

    @classmethod
    def lock_g(cls, name):
        model_name = cls.__name__
        model_name_l = model_name.lower()
        lock_name = "%s_%s" % (model_name_l, name)
        lock = LOCKS_MAP.get(lock_name, threading.RLock())
        lock.acquire()
        LOCKS_MAP[lock_name] = lock

    @classmethod
    def unlock_g(cls, name):
        model_name = cls.__name__
        model_name_l = model_name.lower()
        lock_name = "%s_%s" % (model_name_l, name)
        lock = LOCKS_MAP[lock_name]
        lock.release()

    @classmethod
    def _slugify(cls, text, delim = u"-"):
        result = []
        if not type(text) == unicode: text = text.decode("utf-8")
        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
        for word in _punct_re.split(text.lower()): result.extend(unidecode.unidecode(word).split())
        return unicode(delim.join(result))

    @classmethod
    def _get_timestamp(cls, date = None):
        date = date or datetime.datetime.utcnow()
        date_utc = date.utctimetuple()
        timestamp = calendar.timegm(date_utc)
        return timestamp

    def pre_create(self):
        import account
        self.unique_id = str(uuid.uuid4())
        self.enabled = True
        self.create_date = self.modify_date = time.time()
        self.create_user = self.modify_user = account.Account.get_from_session(raise_e = False)

    def pre_update(self):
        import account
        self.modify_date = time.time()
        self.modify_user = account.Account.get_from_session(raise_e = False)

    def enable_s(self):
        if self.enabled: return
        self.enabled = True
        self.save()
        self.trigger("enabled")

    def disable_s(self):
        if not self.enabled: return
        self.enabled = False
        self.save()
        self.trigger("disabled")

    def increment_s(self, name, default = 0):
        # acquires a lock for the attribute
        self.lock(name)

        # increments the value
        value = getattr(self, name) if hasattr(self, name) else default
        value += 1
        setattr(self, name, value)

        # saves the change and releases the lock
        collection = self._collection()
        try: collection.update({"id" : self.id}, {"$set" : {name : value}})
        finally: self.unlock(name)

    def decrement_s(self, name, default = 0):
        # acquires a lock for the attribute
        self.lock(name)

        # decrements the value
        value = getattr(self, name) if hasattr(self, name) else default
        value -= 1
        setattr(self, name, value)

        # saves the change and releases the lock
        collection = self._collection()
        try: collection.update({"id" : self.id}, {"$set" : {name : value}})
        finally: self.unlock(name)

    def get_previous(self):
        import account
        account_s = account.Account.get_from_session(raise_e = False)
        _class = self.__class__
        entities = _class.find(
            id = {
                "$lt" : self.id
            },
            enabled = True,
            sort = [
                ("id", -1)
            ],
            limit = 1
        ) if account_s else _class.find(
            id = {
                "$lt" : self.id
            },
            sort = [
                ("id", -1)
            ],
            limit = 1
        )
        if not entities: return
        entity = entities[0]
        return entity

    def get_next(self):
        import account
        account_s = account.Account.get_from_session(raise_e = False)
        _class = self.__class__
        entities = _class.find(
            id = {
                "$gt" : self.id
            },
            enabled = True,
            sort = [
                ("id", 1)
            ],
            limit = 1
        ) if account_s else _class.find(
            id = {
                "$gt" : self.id
            },
            sort = [
                ("id", 1)
            ],
            limit = 1
        )
        if not entities: return
        entity = entities[0]
        return entity

    def get_previous_id(self):
        previous = self.get_previous()
        if not previous: return
        return previous.id

    def get_next_id(self):
        next = self.get_next()
        if not next: return
        return next.id

    def lock(self, name = None):
        _name = "%d_%s" % (self.id, name or "")
        self.lock_g(_name)

    def unlock(self, name = None):
        _name = "%d_%s" % (self.id, name or "")
        self.unlock_g(_name)

    def reload(self):
        cls = self.__class__
        return cls.get(id = self.id)

    def equals(self, entity):
        self_id = self.id if hasattr(self, "id") else None
        entity_id = entity.id if hasattr(entity, "id") else None
        return self_id == entity_id

    def is_persisted(self):
        return hasattr(self, "id") and not self.id == None

    def is_modified(self):
        return not self.create_date == self.modify_date

    def has_previous(self):
        previous = self.get_previous()
        return bool(previous)

    def has_next(self):
        next = self.get_next()
        return bool(next)

    def has(self, name):
        if not hasattr(self, name): return False
        if not self.name: return False
        return True
