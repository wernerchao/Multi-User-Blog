import os
import jinja2
import webapp2
import re
import hmac
import hashlib
import random
from string import letters

from google.appengine.ext import db

SECRET = 'wernerhelloch@ou$ingthisasmysecrethahaha'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

# A normal out print with jinja
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Doing some hashing using hmac to hash the input value
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    temp = h.split("|")
    if hash_str(temp[0]) == temp[1]:
        return temp[0]
    else:
        None

# Main handler of all things, used this as parent for other classes to extend
class Handler(webapp2.RequestHandler):
    # def write(self, *a, **kw):
    #     self.response.out.write(*a, **kw)
    # Kind of unnecessary to use this helper function

    def render_str(self, template, **params):
        # t = jinja_env.get_template(template), kind of unnecessary
        # return t.render(**kw) # kind of unnecessary # return a string
        params['user'] = self.user
        return jinja_env.get_template(template).render(**params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
        # Call the write function, and pass in render_str results as argument

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

##### User stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name =', name).get()
        return u

    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u

class MainPage(Handler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_val = self.request.cookies.get('visits')
        if visit_cookie_val:
            cookie_val = check_secure_val(visit_cookie_val) #if check failed, returns None
            if cookie_val:
                visits = int(cookie_val) #if above check failed, visits = int(None), which is 0

        visits += 1

        new_cookie_val = make_secure_val(str(visits))

        self.response.headers.add_header('Set-Cookie', 'visits = %s' % new_cookie_val)
        self.response.out.write("You've been here %s times" % visits)

class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = n and int(n)
        self.render('fizzbuzz.html', n = n)

class ROT13Handler(Handler):
    def get(self):
        temp = ""
        content = self.request.get("content")
        for char in content:
            stringNumber = ord(char)
            rot13 = stringNumber + 13
            if stringNumber > 64 and stringNumber < 91: #capital letter conversion
                if rot13 > 90:
                    rot13 = rot13 - 90 + 64
                rot13 = chr(rot13)
                temp += rot13
            elif stringNumber > 96 and stringNumber < 123: #non-capital letter conversion
                if rot13 > 122:
                    rot13 = rot13 - 122 + 96
                rot13 = chr(rot13)
                temp += rot13
            else:
                temp += char
        self.render('ROT13.html', content = temp)

# Some simple validation methods to check username, password, and email.
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

### Signup and welcome page here

# Handle the signup page
class SignUpHandler(Handler):
    def valid_username(self, username):
        return username and USER_RE.match(username)

    def valid_password(self, password):
        return password and PASSWORD_RE.match(password)

    def valid_email(self, email):
        return not email or EMAIL_RE.match(email)

    def get(self):
        self.render("signup.html")

    def post(self):
        have_error = False
        self.username = self.request.get("username")
        self.password = self.request.get("password")
        self.verifyPassword = self.request.get("verifyPassword")
        self.email = self.request.get("email")

        params = dict(username = self.username, email = self.email)

        if not (self.valid_username(self.username)):
            params['error_username'] = "Not valid username"
            have_error = True

        if not (self.valid_password(self.password)):
            params['error_password'] = "Not valid password"
            have_error = True
        elif self.password != self.verifyPassword:
             params['error_verify'] = "Passwords didn't match.'"
             have_error = True
        
        if not (self.valid_email(self.email)):
            params['error_email'] = "Not valid email"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError

# Check if the user already exists or not when registering. Extends the SignUpHandler class.
class Register(SignUpHandler):
    def done(self):
        # Make sure the user doesn't already exist
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('signup.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            # This login function actually just sets the cookie.
            self.login(u)
            self.redirect("/welcome")

# After the user signs up, will be redirected to a welcome page with his name displayed.
class WelcomeHandler(Handler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')

class LoginHandler(Handler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

class LogoutHandler(Handler):
    def get(self):
        self.logout()
        self.redirect('/blog')

### Blog stuff starts here

# Handles how each post is displayed
class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_by = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self)

# Handles the home page of the blog
class BlogHandler(Handler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10 ")
        self.render("blog.html", posts = posts)

# Handles the new single post the user just submitted
class PostPageHandler(Handler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        self.render("post_page.html", post = post)

# Handles the form to take in new input post
class NewPostHandler(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            p = Post(title = title, content = content, created_by = self.user.name)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "We need both title and content"
            self.render("newpost.html", title = title, content = content, error = error)

# Handles the delete button click to delete the specific post
class DeletePostHandler(Handler):
    def post(self):
        key = self.request.get("key")
        item = db.get(key)
        db.delete(item)
        self.response.out.write("Your post '%s' has been successfully deleted" %key)

# Handles the edit button click to edit the specific post
class EditPostHandler(Handler):
    def get(self):
        key = self.request.get("key")
        item = db.get(key)
        # if self.user.name == "werner":
        self.render("editpost.html", title = item.title, content = item.content, key = key, created_by = item.created_by)
        # else:
        #     self.render("blog.html", error = "You don't have the permission to edit this post'")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        key = self.request.get("key")
        item = db.get(key)
        if title and content:
            item.title = title
            item.content = content
            item.put()
            # self.response.out.write("Your post: '%s'." %title)
            self.redirect('/blog/%s' % str(item.key().id()))
        else:
            error = "We need both title and content"
            # self.render("newpost.html", title = title, content = content, error = error)

app = webapp2.WSGIApplication([
                                ('/', MainPage), 
                                ('/fizzbuzz', FizzBuzzHandler),
                                ('/ROT13', ROT13Handler),
                                ('/signup', Register),
                                ('/welcome', WelcomeHandler),
                                ('/login', LoginHandler),
                                ('/logout', LogoutHandler),
                                ('/blog/?', BlogHandler),
                                ('/blog/([0-9]+)', PostPageHandler),
                                ('/blog/newpost', NewPostHandler),
                                ('/blog/editpost', EditPostHandler),
                                ('/blog/deletepost', DeletePostHandler)
                                ], debug=True)
