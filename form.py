import webapp2

form = """
<form method="post">
    What is your birthday?
    <br>
    <label>Month <input type="text" name="month"></label>
    <label>Day <input type="text" name="day"></label>
    <label>Year <input type="text" name="year"></label>
    <br>
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(form)

class TestHandler(webapp2.RequestHandler):
    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        self.response.out.write("Thanks!")

app = webapp2.WSGIApplication([('/', MainPage), ('/', TestHandler)], debug=True)

# dev_appserver.py app.yaml