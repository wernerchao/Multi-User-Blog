from handlers import Handler
from google.appengine.ext import db

from models import Comment


class CommentPostHandler(Handler):
    """ Handles the comment input on each post.
    Uses the same edit/delete functionalities as the Post model."""

    def post(self):
        comment = self.request.get("comment")
        key = self.request.get("key")
        item = db.get(key)

        if key:  # Checks if the post exists in the database or not.
            if self.user:  # Checks if the user is logged in or not.
                if comment:

                    # Use the Comment model (comment.html),
                    # which uses the same edit/delete functionalities
                    # as Post model (post.html)
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
