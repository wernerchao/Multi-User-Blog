from handlers import Handler
from google.appengine.ext import db

from models import Comment

# Handles the comment input on each post.
class CommentPostHandler(Handler):
    def post(self):
        comment = self.request.get("comment")
        key = self.request.get("key")
        item = db.get(key)

        if key:
            if self.user:
                if comment:
                    p = Comment(parent=item.key(),
                                title='none',
                                content=comment,
                                created_by=self.user.name)
                    p.put()
                    return self.redirect('/blog')
                else:
                    return self.response.out.write(
                        "You can't submit an empty comment")
            else:
                return self.redirect('/signup')
        else:
            self.response.out.write('Your post does not exist!')