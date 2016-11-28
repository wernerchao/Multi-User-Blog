import time
from handlers import Handler
from google.appengine.ext import db

# Handles the edit button click to edit the specific post.
class EditPostHandler(Handler):
    def get(self):
        key = self.request.get("key")
        item = db.get(key)
        if key:
            if self.user:
                if item.created_by == self.user.name:
                    self.render("editpost.html",
                                title=item.title,
                                content=item.content,
                                key=key,
                                created_by=item.created_by)
                else:
                    self.render('editpost.html', post=item)
            else:
                self.redirect('/signup')
        else:
            self.response.out.write("Your post doesn't exist!'")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        key = self.request.get("key")
        item = db.get(key)
        if key:
            if title and content:
                item.title = title
                item.content = content
                item.put()
                time.sleep(0.1)
                return self.redirect('/blog')
            else:
                error = "We need both title and content"
        else:
            self.response.out.write("Your post doesn't exist!")