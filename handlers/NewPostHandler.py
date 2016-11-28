from handlers import Handler
from models import Post

# Handles the form to take in new input post.
class NewPostHandler(Handler):
    def get(self):
        if self.user:
            self.render("newpost.html")
        else:
            # self.response.out.write("You need to login!")
            self.render('signup.html', error_general="Please signup or login")

    def post(self):
        if self.user:
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
            # self.response.out.write("You need to login!")
            self.render('signup.html', error_general="Please signup or login")