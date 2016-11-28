import os
import jinja2
import webapp2
import re
# import hmac
import time

from google.appengine.ext import db

### Model Refactoring
from models import User, Post, Comment

### Handler Refactoring
from handlers import Handler
from handlers import MainPage, BlogHandler
from handlers import SignUpHandler, Register
from handlers import LoginHandler, LogoutHandler
from handlers import PostPageHandler, NewPostHandler
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


### Refactoring to Handler.py
# SECRET = 'wernerhelloch@ou$ingthisasmysecrethahaha'

### Refactoring to Handler.py
# template_dir = os.path.join(os.path.dirname(__file__), 'templates')
# jinja_env = jinja2.Environment(
#     loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


### Only used by class Handler, Refactoring to Handler.py
# Doing hashing using hmac to hash the input value.
# def hash_str(s):
#     return hmac.new(SECRET, s).hexdigest()


# def make_secure_val(s):
#     return "%s|%s" % (s, hash_str(s))


# def check_secure_val(h):
#     temp = h.split("|")
#     if hash_str(temp[0]) == temp[1]:
#         return temp[0]
#     else:
#         None

### Refactoring to Handler.py
# Main handler of all things, used this as parent for other classes to extend.
# class Handler(webapp2.RequestHandler):
#     def render_str(self, template, **params):
#         params['user'] = self.user
#         return jinja_env.get_template(template).render(**params)

#     # Call the write function, and pass in render_str results as argument.
#     def render(self, template, **kw):
#         self.response.out.write(self.render_str(template, **kw))

#     def set_secure_cookie(self, name, val):
#         cookie_val = make_secure_val(val)
#         self.response.headers.add_header(
#             'Set-Cookie',
#             '%s=%s; Path=/' % (name, cookie_val))

#     def read_secure_cookie(self, name):
#         cookie_val = self.request.cookies.get(name)
#         return cookie_val and check_secure_val(cookie_val)

#     def login(self, user):
#         self.set_secure_cookie('user_id', str(user.key().id()))

#     def logout(self):
#         self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

#     def initialize(self, *a, **kw):
#         webapp2.RequestHandler.initialize(self, *a, **kw)
#         uid = self.read_secure_cookie('user_id')
#         self.user = uid and User.by_id(int(uid))


### Refactoring to User.py file
# User stuff starts here.
# def make_salt(length=5):
#     return ''.join(random.choice(letters) for x in xrange(length))


# def make_pw_hash(name, pw, salt=None):
#     if not salt:
#         salt = make_salt()
#     h = hashlib.sha256(name + pw + salt).hexdigest()
#     return '%s,%s' % (salt, h)


# def valid_pw(name, password, h):
#     salt = h.split(',')[0]
#     return h == make_pw_hash(name, password, salt)


# def users_key(group='default'):
#     return db.Key.from_path('users', group)


# class User(db.Model):
#     name = db.StringProperty(required=True)
#     pw_hash = db.StringProperty(required=True)
#     email = db.StringProperty()

#     @classmethod
#     def by_id(cls, uid):
#         return User.get_by_id(uid, parent=users_key())

#     @classmethod
#     def by_name(cls, name):
#         u = User.all().filter('name =', name).get()
#         return u

#     @classmethod
#     def register(cls, name, pw, email=None):
#         pw_hash = make_pw_hash(name, pw)
#         return User(parent=users_key(),
#                     name=name,
#                     pw_hash=pw_hash,
#                     email=email)

#     @classmethod
#     def login(cls, name, pw):
#         u = cls.by_name(name)
#         if u and valid_pw(name, pw, u.pw_hash):
#             return u


### Refactoring to MainPage.py
# class MainPage(Handler):
#     def get(self):
#         if self.user:
#             self.render('welcome.html', username=self.user.name)
#         else:
#             self.redirect('/signup')


### Refactoring to SignUpHandler.py
# Validates the username, password, and email format.
# USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
# PASSWORD_RE = re.compile(r"^.{3,20}$")
# EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


### Refactoring to SignUpHandler.py
# Signup, login, and logout stuff starts here.
# Basic signup handler to be used/extended by register.
# class SignUpHandler(Handler):
#     def valid_username(self, username):
#         return username and USER_RE.match(username)

#     def valid_password(self, password):
#         return password and PASSWORD_RE.match(password)

#     def valid_email(self, email):
#         return not email or EMAIL_RE.match(email)

#     def get(self):
#         self.render("signup.html")

#     def post(self):
#         have_error = False
#         self.username = self.request.get("username")
#         self.password = self.request.get("password")
#         self.verifyPassword = self.request.get("verifyPassword")
#         self.email = self.request.get("email")

#         params = dict(username=self.username, email=self.email)

#         if not (self.valid_username(self.username)):
#             params['error_username'] = "Not valid username"
#             have_error = True

#         if not (self.valid_password(self.password)):
#             params['error_password'] = "Not valid password"
#             have_error = True
#         elif self.password != self.verifyPassword:
#             params['error_verify'] = "Passwords didn't match.'"
#             have_error = True

#         if not (self.valid_email(self.email)):
#             params['error_email'] = "Not valid email"
#             have_error = True

#         if have_error:
#             self.render('signup.html', **params)
#         else:
#             self.done()

#     def done(self, *a, **kw):
#         raise NotImplementedError


# Check if the user already exists or not when registering.
# Extends the SignUpHandler class.
# class Register(SignUpHandler):
#     def done(self):
#         # Make sure the user doesn't already exist.
#         u = User.by_name(self.username)
#         if u:
#             msg = 'That user already exists.'
#             self.render('signup.html', error_username=msg)
#         else:
#             u = User.register(self.username, self.password, self.email)
#             u.put()

#             # This login function actually just sets the cookie.
#             self.login(u)
#             self.redirect("/")


### Refactoring to LoginLogouHandler.py
# class LoginHandler(Handler):
#     def get(self):
#         self.render('login-form.html')

#     def post(self):
#         username = self.request.get('username')
#         password = self.request.get('password')

#         u = User.login(username, password)
#         if u:
#             self.login(u)
#             self.redirect('/blog')
#         else:
#             msg = 'Invalid login'
#             self.render('login-form.html', error=msg)


# class LogoutHandler(Handler):
#     def get(self):
#         self.logout()
#         self.redirect('/blog')


### Model refactoring to Post.py
# Blog stuff starts here.
# Handles how each post is displayed.
# class Post(db.Model):
#     title = db.StringProperty(required=True)
#     content = db.TextProperty(required=True)
#     likes = db.IntegerProperty(required=False)
#     liked_by = db.ListProperty(str)
#     created_by = db.StringProperty(required=False)
#     created = db.DateTimeProperty(auto_now_add=True)
#     last_modified = db.DateTimeProperty(auto_now=True)

#     def render(self):
#         comments = Comment.all().ancestor(self).order("created").fetch(10)
#         self._render_text = self.content.replace('\n', '<br>')
#         return render_str("post.html", p=self, comments=comments)


### Model refactoring to Comment.py
# Handles how each comment is displayed.
# class Comment(db.Model):
#     title = db.StringProperty(required=True)
#     content = db.TextProperty(required=True)
#     created_by = db.StringProperty(required=False)
#     created = db.DateTimeProperty(auto_now_add=True)
#     last_modified = db.DateTimeProperty(auto_now=True)

#     def render(self):
#         self._render_text = self.content.replace('\n', '<br>')
#         return render_str("comment.html", p=self)

### Refactoring to BlogHandler.py
# Handles the home page of the blog, which is the "/blog" url.
# class BlogHandler(Handler):
#     def get(self):
#         posts = db.GqlQuery(
#             "select * from Post order by created desc limit 10 ")
#         self.render("blog.html", posts=posts)


### Refactoring to PostPageHandler.py
# Handles the new single post the user just submitted.
# class PostPageHandler(Handler):
#     def get(self, post_id):
#         key = db.Key.from_path('Post', int(post_id))
#         post = db.get(key)
#         self.render("post_page.html", post=post)


### Refactoring to NewPostHandler
# Handles the form to take in new input post.
# class NewPostHandler(Handler):
#     def get(self):
#         if self.user:
#             self.render("newpost.html")
#         else:
#             # self.response.out.write("You need to login!")
#             self.render('signup.html', error_general="Please signup or login")

#     def post(self):
#         if self.user:
#             title = self.request.get("title")
#             content = self.request.get("content")
#             liked_by = [self.user.name]

#             if title and content:
#                 p = Post(title=title,
#                         content=content,
#                         created_by=self.user.name,
#                         likes=0,
#                         liked_by=liked_by)
#                 p.put()
#                 self.redirect('/blog/%s' % str(p.key().id()))
#             else:
#                 error = "We need both title and content"
#                 self.render("newpost.html", title=title,
#                             content=content, error=error)
#         else:
#             # self.response.out.write("You need to login!")
#             self.render('signup.html', error_general="Please signup or login")


### Refactoring to DeletePostHandler.py
# Handles the delete button click to delete the specific post.
# class DeletePostHandler(Handler):
#     def post(self):
#         key = self.request.get("key")
#         item = db.get(key)
#         if key:
#             if self.user:
#                 if item.created_by == self.user.name:
#                     db.delete(item)
#                     self.render('deletepost.html', post=item)
#                 else:
#                     self.render('deletepost.html', post=item)
#             else:
#                 return self.redirect('/signup')
#         else:
#             self.render('deletepost.html', post=item)


### Refactoring to EditPostHandler
# Handles the edit button click to edit the specific post.
# class EditPostHandler(Handler):
#     def get(self):
#         key = self.request.get("key")
#         item = db.get(key)
#         if key:
#             if self.user:
#                 if item.created_by == self.user.name:
#                     self.render("editpost.html",
#                                 title=item.title,
#                                 content=item.content,
#                                 key=key,
#                                 created_by=item.created_by)
#                 else:
#                     self.render('editpost.html', post=item)
#             else:
#                 self.redirect('/signup')
#         else:
#             self.response.out.write("Your post doesn't exist!'")

#     def post(self):
#         title = self.request.get("title")
#         content = self.request.get("content")

#         key = self.request.get("key")
#         item = db.get(key)
#         if key:
#             if title and content:
#                 item.title = title
#                 item.content = content
#                 item.put()
#                 time.sleep(0.1)
#                 return self.redirect('/blog')
#             else:
#                 error = "We need both title and content"
#         else:
#             self.response.out.write("Your post doesn't exist!")


### Refactoring to LikePostHandler.py
# Handles the like+1 button click.
# class LikePostHandler(Handler):
#     def post(self):
#         key = self.request.get("key")
#         item = db.get(key)
#         liked_dict = {x: x for x in item.liked_by}
#         if key:
#             if self.user:
#                 exist = self.user.name in liked_dict.keys()
#                 if exist: # Check if the user already liked the post OR the user is the post owner
#                     self.response.out.write(
#                         "You don't have permission to like this post")
#                 else:
#                     item.liked_by.append(self.user.name)
#                     item.likes += 1
#                     item.put()
#                     time.sleep(0.1)
#                     return self.redirect('/blog')
#             else:
#                 return self.redirect('/signup')
#         else:
#             self.response.out.write("Your post doesn't exist!")


### Refactoring to CommentPostHandler.py
# Handles the comment input on each post.
# class CommentPostHandler(Handler):
#     def post(self):
#         comment = self.request.get("comment")
#         key = self.request.get("key")
#         item = db.get(key)

#         if key:
#             if self.user:
#                 if comment:
#                     p = Comment(parent=item.key(),
#                                 title='none',
#                                 content=comment,
#                                 created_by=self.user.name)
#                     p.put()
#                     return self.redirect('/blog')
#                 else:
#                     return self.response.out.write(
#                         "You can't submit an empty comment")
#             else:
#                 return self.redirect('/signup')
#         else:
#             self.response.out.write('Your post does not exist!')
