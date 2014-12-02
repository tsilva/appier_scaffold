#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

import models

class BaseController(appier.Controller):

    @appier.route("/", "GET")
    def index(self):
        account_s = models.Account.get_from_session(raise_e = False)
        success = self.field("success")
        return self.template(
            "index.html.tpl",
            link = "home",
            account_s = account_s,
            success = success
        )

    @appier.route("/robots.txt", "GET")
    def robots(self):
        return self.template(
            "robots.txt"
        )

    @appier.route("/login", "GET")
    def login(self):
        account_s = models.Account.get_from_session(raise_e = False)
        success = self.field("success")
        error = self.field("error")
        next = self.field("next")
        return self.template(
            "signin.html.tpl",
            link = "signin",
            account_s = account_s,
            success = success,
            error = error,
            next = next
        )

    @appier.route("/login", "POST")
    def login_post(self):
        # retrieves the session account
        account_s = models.Account.get_from_session(raise_e = False)

        # retrieves the auth parameters
        email = self.field("email")
        password = self.field("password")
        next = self.field("next")

        # performs the login
        try: account = models.Account.login(email, password)
        except appier.exceptions.OperationalError, error:
            return self.template(
                "signin.html.tpl",
                account_s = account_s,
                email = email,
                next = next,
                error = error.message
            )

        # sets the account in the session
        account.set_in_session()
        
        # redirects to the correct url
        if not next: next = self.url_for("base.index")
        return self.redirect(next)

    @appier.route("/logout", ("GET", "POST"))
    def logout(self):
        models.Account.clear_session()
        return self.redirect(
            self.url_for("base.index")
        )

    @appier.route("/signup", "GET")
    def signup_get(self):
        account_s = models.Account.get_from_session(raise_e = False)
        success = self.field("success")
        return self.template(
            "signup.html.tpl",
            link = "signup",
            account_s = account_s,
            account = {},
            errors = {},
            success = success
        )

    @appier.route("/signup", "POST")
    def signup_post(self):
        # retrieves the session account
        account_s = models.Account.get_from_session(raise_e = False)

        # attempts to create a new account
        account = models.Account.new()
        try: account.save()
        except appier.exceptions.ValidationError, error:
            return self.template(
                "signup.html.tpl",
                account_s = account_s,
                account = error.model,
                errors = error.errors
            )

        # sends the signup email
        account.send_signup_email_s()
        return self.redirect(
            self.url_for(
                "base.signup_get",
                success = "An email was sent with instructions on how to confirm your account and login."
            )
        )

    @appier.route("/confirm", "GET")
    def confirm(self):
        confirmation_code = self.field("confirmation_code")
        models.Account.confirm_s(confirmation_code)
        return self.redirect(
            self.url_for(
                "base.index",
                success = "Your account was confirmed successfully."
            )
        )

    @appier.route("/recover", "GET")
    def recover_get(self):
        account_s = models.Account.get_from_session(raise_e = False)
        success = self.field("success")
        return self.template(
            "recover.html.tpl",
            link = "recover",
            account_s = account_s,
            success = success
        )

    @appier.route("/recover", "POST")
    def recover_post(self):
        # retrieves the session account
        account_s = models.Account.get_from_session(raise_e = False)

        # attempts to retrieve the specified account
        email = self.field("email")
        try: account = models.Account.get(email = email)
        except: return self.template(
            "recover.html.tpl",
            account_s = account_s,
            email = email,
            error = "No matching account found"
        )

        # sends the recovery email
        account.send_recovery_email_s()

        # redirects back to the recover
        # page with a success message
        return self.redirect(
            self.url_for(
                "base.recover_get",
                success = "An email was sent with instructions on how to recover your account."
            )
        )

    @appier.route("/reset", "GET")
    def reset_get(self):
        account_s = models.Account.get_from_session(raise_e = False)
        reset_code = self.field("reset_code")
        models.Account.get(reset_code = reset_code)
        return self.template(
            "reset.html.tpl",
            link = "reset",
            account_s = account_s,
            reset_code = reset_code,
            account = {},
            errors = {}
        )

    @appier.route("/reset", "POST")
    def reset_post(self):
        # retrieves the session account
        account_s = models.Account.get_from_session(raise_e = False)

        # resets the account with the provided reset code
        reset_code = self.field("reset_code")
        try: models.Account.reset_s(reset_code)
        except appier.exceptions.ValidationError, error:
            return self.template(
                "reset.html.tpl",
                account_s = account_s,
                reset_code = reset_code,
                account = error.model,
                errors = error.errors,
                error = "Please insert a valid password (more than 5 characters, lowercase, no spaces, starting with a letter)"
            )

        # redirects to the signin page
        return self.redirect(
            self.url_for(
                "base.login",
                success = "Your password was changed successfully."
            )
        )

    @appier.route("/about", "GET")
    def about(self):
        account_s = models.Account.get_from_session(raise_e = False)
        return self.template(
            "about.html.tpl",
            link = "about",
            account_s = account_s
        )

    @appier.error_handler(403)
    def error_403(self, error):
        return self.redirect(
            self.url_for(
                "base.login",
                error = "Unauthorized, please login first."
            )
        )

    @appier.error_handler(404)
    def error_404(self, error):
        account_s = models.Account.get_from_session(raise_e = False)
        return self.template(
            "error_404.html.tpl",
            account_s = account_s
        )

    @appier.error_handler(500)
    def error_500(self, error):
        account_s = models.Account.get_from_session(raise_e = False)
        return self.template(
            "error_500.html.tpl",
            account_s = account_s
        )
