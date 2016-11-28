import time
from handlers import Handler
from google.appengine.ext import db


# Handles the like+1 button click.
class LikePostHandler(Handler):
    """ Handles the like+1 button click for each blog post.
    Users cannot like own post, and each user can only like a post once """

    def post(self):
        key = self.request.get("key")
        item = db.get(key)
        liked_dict = {x: x for x in item.liked_by}
        if key:  # First check if the post exists or not.
            if self.user:  # Check if the user is logged in or not.

                # This allows us to check if the user
                # already liked the post OR the user is the post owner
                exist = self.user.name in liked_dict.keys()

                # If the user already liked thepost OR
                # the user is the post owner
                if exist:
                    self.response.out.write(
                        "You don't have permission to like this post")

                # If the user hasn't liked the post OR
                # the user is not the post owner
                else:
                    item.liked_by.append(self.user.name)
                    item.likes += 1
                    item.put()
                    time.sleep(0.1)
                    return self.redirect('/blog')
            else:
                return self.redirect('/signup')
        else:
            self.response.out.write("Your post doesn't exist!")
