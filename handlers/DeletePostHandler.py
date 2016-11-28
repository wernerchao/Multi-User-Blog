from handlers import Handler
from google.appengine.ext import db

# Handles the delete button click to delete the specific post.
class DeletePostHandler(Handler):
    def post(self):
        key = self.request.get("key")
        item = db.get(key)
        if key:
            if self.user:
                if item.created_by == self.user.name:
                    db.delete(item)
                    self.render('deletepost.html', post=item)
                else:
                    self.render('deletepost.html', post=item)
            else:
                return self.redirect('/signup')
        else:
            self.render('deletepost.html', post=item)