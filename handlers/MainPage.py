from handlers import Handler

class MainPage(Handler):
    """ Handles the main welcome page (/signup) """

    def get(self):
        if self.user:
            self.render('welcome.html', username=self.user.name)
        else:
            self.redirect('/signup')