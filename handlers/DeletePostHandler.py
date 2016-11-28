from handlers import Handler
from google.appengine.ext import db


class DeletePostHandler(Handler):
    """ Handles the delete button click to
    delete the specific post/comment.
    Only the post/comment owner can delete the post/comment. """

    def post(self):
        key = self.request.get("key")
        item = db.get(key)
        if key:  # Checks if the post exists in the database or not.
            if self.user:  # Checks if the user is logged in or not.
                if item.created_by == self.user.name:
                    db.delete(item)
                    self.render('deletepost.html', post=item)
                else:
                    self.render('deletepost.html', post=item)
            else:
                return self.redirect('/signup')
        else:
            self.render('deletepost.html', post=item)
