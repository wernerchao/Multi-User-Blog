from handlers import Handler
from google.appengine.ext import db

# Handles the home page of the blog, which is the "/blog" url.
class BlogHandler(Handler):
    def get(self):
        posts = db.GqlQuery(
            "select * from Post order by created desc limit 10 ")
        self.render("blog.html", posts=posts)