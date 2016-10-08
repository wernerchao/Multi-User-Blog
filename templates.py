import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    # def write(self, *a, **kw):
    #     self.response.out.write(*a, **kw)
    #kind of unnecessary to use this helper function

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        # return t.render(**kw), kind of unnecessary
        # return a string
        return jinja_env.get_template(template).render(**kw)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))
        # call the write function, and pass in render_str results as argument
        # template is shopping_list.html

class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food") #get food query parameter from the url
        self.render("shopping_list.html", items = items)

        # n = self.request.get("n")
        # if n and n.isdigit():
        #     n = int(n)
        # self.render("shopping_list.html", n = n)

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

app = webapp2.WSGIApplication([
                                ('/', MainPage), 
                                ('/fizzbuzz', FizzBuzzHandler),
                                ('/ROT13', ROT13Handler)
                                ], debug=True)

# app = webapp2.WSGIApplication([('/', MainPage)], debug=True)