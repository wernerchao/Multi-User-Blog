from handlers import Handler
from google.appengine.ext import db

# Handles the new single post the user just submitted.
class PostPageHandler(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        self.render("post_page.html", post=post)