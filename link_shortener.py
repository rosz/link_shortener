import random
import tornado.ioloop
from tornado.web import RequestHandler


class ShortenUrl(RequestHandler):
    # receive original link
    def post(self):
        link_original = self.request.body
        self.write(link_original)

    # return shortened link
    def get(self):
        self.write("Link not found in data base. Invalid or expired link")


def make_app():
    return tornado.web.Application([
        (r"/", ShortenUrl),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
