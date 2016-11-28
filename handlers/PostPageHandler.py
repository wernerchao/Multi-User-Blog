from handlers import Handler
from google.appengine.ext import db


class PostPageHandler(Handler):
    """ Handles the new single post that the user just submitted. """

    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        self.render("post_page.html", post=post)
