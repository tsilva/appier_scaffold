#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time
import uuid
import hashlib
import datetime

import appier

import base

SALT_SIZE = 12
""" The size of the password salts """

SALT_SEPARATOR = "$"
""" The character used to separate the salt from the password """

class Account(base.Base):

    email = dict(
        index = True
    )

    # @TODO: private?
    password = dict()

    confirmation_code = dict(
        index = True
    )

    confirmation_code_date = dict(
        type = int
    )

    reset_code = dict(
        index = True
    )

    reset_code_date = dict(
        type = int
    )

    name = dict()

    name_l = dict(
        index = True
    )

    birth_date = dict(
        type = int
    )

    @classmethod
    def validate(cls):
        return super(Account, cls).validate() + [
            appier.not_null("email"),
            appier.not_empty("email"),
            appier.is_email("email"),
            appier.not_duplicate("email", cls._name()),

            appier.not_null("name"),
            appier.not_empty("name")
        ]

    @classmethod
    def validate_password_set(cls):
        return [
            appier.not_null("_password"),
            appier.not_empty("_password")
        ]

    @classmethod
    def validate_password_strength(cls):
        return [
            appier.string_gt("_password", 5)
        ]

    @classmethod
    def validate_password_confirm(cls):
        return [
            appier.not_null("_password_confirm"),
            appier.not_empty("_password_confirm"),
            appier.field_eq("_password_confirm", "_password")
        ]

    @classmethod
    def clear_session(self):
        _account = Account()
        if "email" in _account.session: del _account.session["email"]
        if "tokens" in _account.session: del _account.session["tokens"]

    @classmethod
    def confirm_s(cls, confirmation_code):
        # raises an exception in case no
        # confirmation code was provided
        if not confirmation_code: raise appier.exceptions.OperationalError(
            message = "no confirmation code was specified",
            code = 403
        )

        # retrieves the account and raises an exception
        # in case the confirmation code has expired
        account = Account.get(
            confirmation_code = confirmation_code,
            enabled = False
        )
        if account.is_confirmation_expired(): raise appier.exceptions.OperationalError(
            message = "confirmation code expired",
            code = 403
        )

        # enables the account now that it's confirmed
        account.confirmation_code = None
        account.confirmation_code_date = None
        account.enable_s()

        # sets the account in the session
        account.set_in_session()

        # returns the account
        return account

    @classmethod
    def reset_s(cls, reset_code):
        # raises an exception in case no
        # reset code was provided
        if not reset_code: raise appier.exceptions.OperationalError(
            message = "no reset code was specified",
            code = 403
        )

        # retrieves the account and raises an exception
        # in case the reset code has expired
        account = Account.get(
            reset_code = reset_code
        )
        if account.is_reset_expired(): raise appier.exceptions.OperationalError(
            message = "reset code expired",
            code = 403
        )

        # applies the new password
        # and saves the account
        account.apply()
        account.reset_code = None
        account.reset_expiration_date = None
        account.save()

        # returns the account
        return account

    @classmethod
    def login(cls, email, password):
        if not email or not password:
            raise appier.exceptions.OperationalError(
                message = "Both email and password must be provided",
                code = 400
            )

        account = cls.get(
            email = email,
            enabled = True,
            build = False,
            raise_e = False
        )
        if not account:
            raise appier.exceptions.OperationalError(
                message = "No matching account found",
                code = 403
            )

        salt, _password = account.password.split(SALT_SEPARATOR)
        password_e = Account.encrypt_password(password, salt)
        if not password_e == account.password:
            raise appier.exceptions.OperationalError(
                message = "Invalid or mismatch password",
                code = 403
            )

        return account

    @classmethod
    def encrypt_password(cls, password, salt = None):
        salt = salt or os.urandom(SALT_SIZE).encode("hex")
        password = "%s%s" % (salt, password)
        password_hash = hashlib.sha256(password)
        password_digest = password_hash.hexdigest()
        password_e = "%s$%s" % (salt, password_digest)
        return password_e

    @classmethod
    def get_from_session(cls, raise_e = True):
        _account = Account()
        email = _account.session.get("email", None)
        if not email and not raise_e: return
        elif not email: raise appier.exceptions.OperationalError(
            message = "no account in session",
            code = 403
        )
        account = cls.get(email = email, enabled = True, raise_e = raise_e)
        return account

    def pre_validate(self):
        base.Base.pre_validate(self)

        # in case the account is not created yet
        # then validates that the password is set
        if not self.is_persisted(): self.validate_extra("password_set")

        # in case a password was provided then
        # validates its strength and confirmation
        _password = self._password if hasattr(self, "_password") else None
        if not _password == None: self.validate_extra("password_strength")
        if not _password == None: self.validate_extra("password_confirm")

    def pre_create(self):
        base.Base.pre_create(self)

        # initializes the defaults
        self.enabled = False
        self.is_owner = False

        # encrypts the password (if provided)
        self._encrypt_password()

    def pre_update(self):
        base.Base.pre_update(self)

        # encrypts the password (if provided)
        self._encrypt_password()

    def send_signup_email_s(self):
        # generates the confirmation url
        self._generate_confirmation_code_s()

        # sends the confirmation email
        app_name = appier.conf("APP_NAME", "Test App")
        sender_name = appier.conf("EMAIL_SENDER_NAME", "Administrator")
        sender_email = appier.conf("EMAIL_SENDER_ADDRESS", "test@test.com")
        sender = "%s <%s>" % (sender_name, sender_email)
        self.owner.email(
            "email_signup.html.tpl",
            subject = "Welcome to %s" % app_name,
            sender = sender,
            receivers = [self.email],
            sender_name = sender_name,
            account = self
        )

    def get_confirm_url(self):
        if not self.has("confirmation_code"): return
        base_url = appier.conf("BASE_URL", "http://www.test.pt")
        confirm_url = self.owner.url_for("base.confirm")
        confirm_url = base_url + confirm_url + "?confirmation_code=%s" % self.confirmation_code
        return confirm_url

    def send_recovery_email_s(self):
        # generates the reset url
        self._generate_reset_code_s()

        # sends the recovery email
        app_name = appier.conf("APP_NAME", "Test App")
        sender_name = appier.conf("EMAIL_SENDER_NAME", "Administrator")
        sender_email = appier.conf("EMAIL_SENDER_ADDRESS", "test@test.com")
        sender = "%s <%s>" % (sender_name, sender_email)
        self.owner.email(
            "email_recover.html.tpl",
            subject = "Somebody requested a new password for your %s account" % app_name,
            sender = sender,
            receivers = [self.email],
            sender_name = sender_name,
            account = self
        )

    def get_reset_url(self):
        if not self.has("reset_code"): return
        base_url = appier.conf("BASE_URL", "http://www.test.pt")
        reset_url = self.owner.url_for("base.reset_get")
        reset_url = base_url + reset_url + "?reset_code=%s" % self.reset_code
        return reset_url

    def get_tokens(self):
        return ["base"]

    def set_in_session(self):
        self.session["email"] = self.email
        self.session["tokens"] = self.get_tokens()
        self.session.permanent = True

    def is_session(self):
        account = Account.get_from_session(raise_e = False)
        if not account: return False
        return self.id == account.id

    def is_confirmation_expired(self):
        current_date = datetime.datetime.utcnow()
        current_timestamp = self._get_timestamp(current_date)
        seconds_elapsed = current_timestamp - self.confirmation_code_date
        return seconds_elapsed > 3600

    def is_reset_expired(self):
        current_date = datetime.datetime.utcnow()
        current_timestamp = self._get_timestamp(current_date)
        seconds_elapsed = current_timestamp - self.reset_code_date
        return seconds_elapsed > 3600

    def _generate_confirmation_code_s(self):
        self.confirmation_code = str(uuid.uuid4())
        self.confirmation_code_date = time.time()
        self.save()

    def _generate_reset_code_s(self):
        self.reset_code = str(uuid.uuid4())
        self.reset_code_date = time.time()
        self.save()

    def _encrypt_password(self):
        _password = self._password if hasattr(self, "_password") else None
        if not _password: return
        self.password = Account.encrypt_password(_password)
        self.reset_code = None
        self.reset_code_date = None
