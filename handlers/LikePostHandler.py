from handlers import Handler
from google.appengine.ext import db

# Handles the like+1 button click.
class LikePostHandler(Handler):
    def post(self):
        key = self.request.get("key")
        item = db.get(key)
        liked_dict = {x: x for x in item.liked_by}
        if key:
            if self.user:
                exist = self.user.name in liked_dict.keys()
                if exist: # Check if the user already liked the post OR the user is the post owner
                    self.response.out.write(
                        "You don't have permission to like this post")
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