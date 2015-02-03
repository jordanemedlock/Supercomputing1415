import tornado.ioloop
import tornado.web
from mimetypes import MimeTypes
import urllib
import tornado.escape
import data
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        f = open("../HTML/index.html")
        s = f.read()
        self.write(s)

class FileHandler(tornado.web.RequestHandler):
    def get(self,fileName):
        url = urllib.pathname2url(fileName)
        t = MimeTypes().guess_type(url)
        print t
        self.set_header("Content-Type", '' + t[0] + '; charset="utf-8"')
        f = open("../HTML/" + fileName)
        s = f.read()
        self.write(s)
class MathFiles(tornado.web.RequestHandler):
    def get(self,fileName):
        url = urllib.pathname2url(fileName)
        t = MimeTypes().guess_type(url)
        print t
        self.set_header("Content-Type", '' + t[0] + '; charset="utf-8"')
        f = open("../IPython/Math6/" + fileName)
        s = f.read()
        self.write(s)

class QueryHandler(tornado.web.RequestHandler):
    def get(self, query):
        print "searching"
        data.createNewMathOut()
        book = data.readBook()
        results = data.search(query,book)
        print "here"
        self.write(json.dumps(results))

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/(index\.css|index\.js|Digital%20Aristotle\.png|DA\.png|doge\.png|favicon.ico)", FileHandler),
    (r"/(Math6-[0-9]+\.png)", MathFiles),
    (r"/search/(.*)", QueryHandler)
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()