from handlers import Handler
from models import Post


class NewPostHandler(Handler):
    """ Handles the form that takes in new input post. """

    def get(self):
        if self.user:  # Checks if the user is logged in or not.
            self.render("newpost.html")
        else:
            self.render('signup.html', error_general="Please signup or login")

    def post(self):
        if self.user:  # Checks if the user is logged in or not.
            title = self.request.get("title")
            content = self.request.get("content")
            liked_by = [self.user.name]

            if title and content:
                p = Post(title=title,
                         content=content,
                         created_by=self.user.name,
                         likes=0,
                         liked_by=liked_by)
                p.put()
                self.redirect('/blog/%s' % str(p.key().id()))
            else:
                error = "We need both title and content"
                self.render("newpost.html", title=title,
                            content=content, error=error)
        else:
            self.render('signup.html', error_general="Please signup or login")
