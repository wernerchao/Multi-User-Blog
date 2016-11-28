from handlers import Handler
import re
from models import User

# Validates the username, password, and email format.
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


class SignUpHandler(Handler):
    """ Basic signup handler to be used/extended by register.
    Checks if the input username, password and email are valid. """

    def valid_username(self, username):
        return username and USER_RE.match(username)

    def valid_password(self, password):
        return password and PASSWORD_RE.match(password)

    def valid_email(self, email):
        return not email or EMAIL_RE.match(email)

    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verifyPassword = self.request.get("verifyPassword")
        self.email = self.request.get("email")

        params = dict(username=self.username, email=self.email)

        if not (self.valid_username(self.username)):
            params['error_username'] = "Not valid username"
            have_error = True

        if not (self.valid_password(self.password)):
            params['error_password'] = "Not valid password"
            have_error = True
        elif self.password != self.verifyPassword:
            params['error_verify'] = "Passwords didn't match.'"
            have_error = True

        if not (self.valid_email(self.email)):
            params['error_email'] = "Not valid email"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError


class Register(SignUpHandler):
    """ Checks if the user already exist or not. And sets the cookie. """

    def done(self):
        # Make sure the user doesn't already exist.
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup.html', error_username=msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            # This login function actually just sets the cookie.
            self.login(u)
            self.redirect("/")
