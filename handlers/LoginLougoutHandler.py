from models import User
from handlers import Handler

class LoginHandler(Handler):
    """ Handles the login page (/login). """

    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error=msg)


class LogoutHandler(Handler):
    """ Handles the logout page (/logout). """

    def get(self):
        self.logout()
        self.redirect('/blog')