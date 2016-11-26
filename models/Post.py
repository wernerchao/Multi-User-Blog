import os
import jinja2

from google.appengine.ext import db

# import Comment
from models import Comment

template_dir = os.path.join(os.path.dirname(__file__), 'model-templates')
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir), autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# Blog stuff starts here.
# Handles how each post is displayed.
class Post(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    likes = db.IntegerProperty(required=False)
    liked_by = db.ListProperty(str)
    created_by = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        comments = Comment.all().ancestor(self).order("created").fetch(10)
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self, comments=comments)