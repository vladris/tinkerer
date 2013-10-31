'''
    Blog Server Test
    ~~~~~~~~~~~~~~~~

    Tests serving the static blog posts.

    :copyright: Copyright 2011-2013 by Vlad Riscutia and contributors (see
    CONTRIBUTORS file)
    :license: FreeBSD, see LICENSE file
'''
import os
import sys
import datetime
import time
from multiprocessing import Process
import tinkerer
from tinkertest import utils

try:
    import urllib2 as request
except ImportError as e:
    import urllib.request as request

class NullDevice(object):
    # setup null write
    def write(self, s):
        pass

    # setup null flush
    def flush(self):
        pass


# test serving the blog
class TestServe(utils.BaseTinkererTest):
    # setup the blog to serve
    def setUp(self):
        utils.setup()
        self.new_post = utils.post.create('My Post', datetime.date(2010, 10, 1))
        self.build()

        # silence the SimpleHTTPServer
        self.orig_stderr = sys.stderr
        sys.stderr = NullDevice()

    def tearDown(self):
        utils.cleanup()
        sys.stderr = self.orig_stderr


    # test serve call
    def test_serve(self):
        response = False
        baseUrl = 'http://localhost:8000/'

        # spin off server as a subprocess
        p = Process(target=utils.server.serve, args=(8000, ))
        p.daemon = True
        p.start()

        if p.is_alive():
            time.sleep(10)
            page = request.urlopen(baseUrl)
            response = page.read()

        # assert response received
        self.assertTrue(response)

        if p.is_alive():
            time.sleep(10)
            path = baseUrl + os.path.relpath(utils.TEST_ROOT) + '/blog/html/' + self.new_post.docname + '.html'
            page = request.urlopen(path)
            response = page.read()

        # assert response received
        self.assertTrue(response)

        # clean up server
        p.terminate()

