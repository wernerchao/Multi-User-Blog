import os
import jinja2
import webapp2
import re
import hmac

from google.appengine.ext import db

SECRET = 'iamsosecret'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    # def write(self, *a, **kw):
    #     self.response.out.write(*a, **kw)
    #kind of unnecessary to use this helper function

    def render_str(self, template, **kw):
        # t = jinja_env.get_template(template), kind of unnecessary
        # return t.render(**kw) # kind of unnecessary # return a string
        return jinja_env.get_template(template).render(**kw)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
        # call the write function, and pass in render_str results as argument

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

        # items = self.request.get_all("food") #get food query parameter from the url
        # self.render("shopping_list.html", items = items)

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
        username = self.request.get("username")
        password = self.request.get("password")
        verifyPassword = self.request.get("verifyPassword")
        email = self.request.get("email")

        params = dict(username = username, email = email)

        if not (self.valid_username(username)):
            params['error_username'] = "Not valid username"
            have_error = True

        if not (self.valid_password(password)):
            params['error_password'] = "Not valid password"
            have_error = True
        elif password != verifyPassword:
             params['error_verify'] = "Passwords didn't match.'"
             have_error = True
        
        if not (self.valid_email(email)):
            params['error_email'] = "Not valid email"
            have_error = True

        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect("/welcome?username=" + username)

# After the user signs up, will be redirected to a welcome page with his name displayed.
class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get("username")
        self.render("welcome.html", username = username)

### Blog stuff starts here

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Handles how each post is displayed
class Post(db.Model):
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
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

# Handles the form to take in new inputs
class NewPostHandler(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        title = self.request.get("title")
        content = self.request.get("content")

        if title and content:
            p = Post(title = title, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "We need both title and content"
            self.render("newpost.html", title = title, content = content, error = error)

app = webapp2.WSGIApplication([
                                ('/', MainPage), 
                                ('/fizzbuzz', FizzBuzzHandler),
                                ('/ROT13', ROT13Handler),
                                ('/signup', SignUpHandler),
                                ('/welcome', WelcomeHandler),
                                ('/blog/?', BlogHandler),
                                ('/blog/([0-9]+)', PostPageHandler),
                                ('/blog/newpost', NewPostHandler)
                                ], debug=True)
