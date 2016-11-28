from handlers import Handler
from google.appengine.ext import db


class BlogHandler(Handler):
    """ Handles the home page of the blog, which is the "/blog" url.
    Gets 10 posts from the database and displays them """

    def get(self):
        posts = db.GqlQuery(
            "select * from Post order by created desc limit 10 ")
        self.render("blog.html", posts=posts)
