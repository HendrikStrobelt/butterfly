import json
import os
import socket
import time
import tornado
import tornado.gen
import tornado.web
import tornado.websocket
import urllib
import urlparse


class WebServerHandler(tornado.web.RequestHandler):

  def initialize(self, webserver):
    self._webserver = webserver

  @tornado.web.asynchronous
  @tornado.gen.coroutine
  def get(self, uri):
    '''
    '''
    self._webserver.handle(self)


class WebServer:

  def __init__( self, core, port=2001 ):
    '''
    '''
    self._core = core
    self._port = port

  def start( self ):
    '''
    '''

    ip = socket.gethostbyname('')
    port = self._port

    webapp = tornado.web.Application([
      
      (r'/metainfo/(.*)', WebServerHandler, dict(webserver=self)),
      (r'/data/(.*)', WebServerHandler, dict(webserver=self)),
      # (r'/(.*)', tornado.web.StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__),'../web'), default_filename='index.html'))
  
    ])

    webapp.listen(port, max_buffer_size=1024*1024*150000)

    print 'Starting webserver at \033[93mhttp://' + ip + ':' + str(port) + '\033[0m'

    tornado.ioloop.IOLoop.instance().start()

  @tornado.gen.coroutine
  def handle( self, handler ):
    '''
    '''
    content = None

    splitted_request = handler.request.uri.split('/')

    query = '/'.join(splitted_request[2:])[1:]

    if splitted_request[1] == 'metainfo':

      # content = self._core.get_meta_info(path)
      content = 'metainfo'
      content_type = 'text/html'

    elif splitted_request[1] == 'data':

      parsed_query = urlparse.parse_qs(query)
      datapath = parsed_query['datapath'][0]
      x = parsed_query['x'][0]
      y = parsed_query['y'][0]
      z = parsed_query['z'][0]
      w = parsed_query['w'][0]

      self._core.get(datapath, (x, y, z), (256,256,1), w)



      # this is for actual image data
      # path = '/'.join(splitted_request[2:-1])

      # tile = splitted_request[-1].split('-')

      # x = int(tile[1])
      # y = int(tile[2])
      # z = int(tile[3])
      # w = int(tile[0])

      # content = self._core.get_image(path, x, y, z, w)
      content = 'data'
      content_type = 'text/html'#'image/jpeg'



    # invalid request
    if not content:
      content = 'Error 404'
      content_type = 'text/html'

    # handler.set_header('Cache-Control','no-cache, no-store, must-revalidate')
    # handler.set_header('Pragma','no-cache')
    # handler.set_header('Expires','0')
    handler.set_header('Access-Control-Allow-Origin', '*')
    handler.set_header('Content-Type', content_type)
    handler.write(content)