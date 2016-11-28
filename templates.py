import webapp2

# Model Refactoring to models folder
from models import User, Post, Comment

# Handler Refactoring to handlers folder
from handlers import MainPage, BlogHandler
from handlers import SignUpHandler, Register
from handlers import LoginHandler, LogoutHandler
from handlers import NewPostHandler, PostPageHandler
from handlers import DeletePostHandler, EditPostHandler
from handlers import LikePostHandler, CommentPostHandler


app = webapp2.WSGIApplication([
                                ('/', MainPage),
                                ('/signup', Register),
                                ('/login', LoginHandler),
                                ('/logout', LogoutHandler),
                                ('/blog/?', BlogHandler),
                                ('/blog/([0-9]+)', PostPageHandler),
                                ('/blog/newpost', NewPostHandler),
                                ('/blog/editpost', EditPostHandler),
                                ('/blog/deletepost', DeletePostHandler),
                                ('/blog/likepost', LikePostHandler),
                                ('/blog/commentpost', CommentPostHandler)
                                ], debug=True)
