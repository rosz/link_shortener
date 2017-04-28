import pymongo
import json
import random
import string
import datetime
import tornado.ioloop
from tornado.web import RequestHandler
from tornado.web import HTTPError


client = pymongo.MongoClient()
db = client.database
collection = db.collection
posts = db.posts

# hardcode the global domain of the shortened link
DOMAIN = "localhost:8888/"


def generate_shortcode():
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choice(chars) for i in range(5))


class ShortenUrl(RequestHandler):
    def verify_json(self, header):
        if header.get("Content-Type", "") != "application/json":
            raise HTTPError(400, "wrong format, JSON expected")

    def unify_data(self, body):
        data = body.decode('utf-8')
        try:
            data_dict = json.loads(data)
        except:
            raise HTTPError(400, "wrong format, JSON expected")
        return data_dict

    def post(self):
        self.verify_json(self.request.headers)
        data = self.unify_data(self.request.body)
        # request.body = {"original_link": "link", "days"=int}
        if "original_link" not in data or "days" not in data:
            raise HTTPError(400, "dictionary key not found")

        original_link = data["original_link"]
        days_to_expire = data["days"]

        if days_to_expire > 7:
            self.write("Too long time to keep the link in database. Type less than/equal to 7.")

        else:
            shortcode = generate_shortcode()
            # veify if shortcode doesn't exost already
            while db.posts.find_one({"shortcode": shortcode}):
                shortcode = generate_shortcode()

            expire_date = datetime.datetime.now() + datetime.timedelta(days=days_to_expire)

            # inserting to database: shortcode, link, expire date
            entry = {"shortcode": shortcode, "original_link": original_link, "expire_date": expire_date}
            entry_id = posts.insert_one(entry).inserted_id

            self.write(DOMAIN + shortcode)


class GetLink(RequestHandler):
    def get(self, shortcode):
        # check if shortcode in database
        if shortcode is None:
            self.write("Link not found in database - invalid shortcode.")

        current_time = datetime.datetime.now()
        current_post = db.posts.find_one({"shortcode": shortcode})
        original_link = current_post["original_link"]
        expire_date = current_post["expire_date"]

        if current_time > expire_date:
            db.posts.remove(current_post)
            self.write("Link not found in database - expired.")

        else:
            self.redirect(original_link)


def make_app():
    return tornado.web.Application([
        (r"/shorten_link", ShortenUrl),
        (r"/([^/]+)", GetLink),
    ], db=db)

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
