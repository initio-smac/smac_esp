#import gc

import usocket, os
import uasyncio as asyncio


class Response:
    saveToFileDone = False
    data = ""

    def __init__(self, socket, saveToFile=None):
    #async def save(self, socket, saveToFile=None):
        self._socket = socket
        self._saveToFile = saveToFile
        self._encoding = 'utf-8'

        #if saveToFile is not None:
        #    asyncio.run( self.save(saveToFile) )
        #else:
        #    asyncio.run( self.copyToVariable() )
            
    async def copyToVariable(self):
        CHUNK_SIZE = 512
        res = b""
        data = await self._socket.read(CHUNK_SIZE)
        while data:
            res += data
            data = await self._socket.read(CHUNK_SIZE)
        self.data = str(res, self._encoding)


    async def save(self, saveToFile):
        CHUNK_SIZE = 512  # bytes
        print("saving file")
        with open(saveToFile, 'wb') as outfile:
            data = await self._socket.read(CHUNK_SIZE)
            while data:
                #print(data)
                outfile.write(data)
                data = await self._socket.read(CHUNK_SIZE)
            outfile.close()

        self.close()
        self.saveToFileDone = True
        print("written to file")
            

    def close(self):
        if self._socket:
            self._socket.close()
            self._socket = None

    @property
    async def content(self):
        if self._saveToFile is not None:
            raise SystemError(
                'You cannot get the content from the response as you decided to save it in {}'.format(self._saveToFile))

        try:
            res = b""
            CHUNK_SIZE = 512
            data = await self._socket.read(CHUNK_SIZE)
            while data:
                res += data
                data = await self._socket.read(CHUNK_SIZE)
            return res
        finally:
            self.close()

    @property
    async def text(self):
        con = await self.content
        return str(con, self._encoding)

    def json(self):
        try:
            import ujson
            result = ujson.load(self._socket)
            return result
        finally:
            self.close()


class HttpClient:

    def __init__(self, headers={}):
        self._headers = headers

    async def _write_headers(self, sock, _headers):
        for k in _headers:
            sock.write(b'{}: {}\r\n'.format(k, _headers[k]))
            await sock.drain()

    async def request(self, method, url, data=None, json=None, file=None, custom=None, saveToFile=None, headers={},
                stream=None):

        await asyncio.sleep(0)
        ssl = False
        try:
            proto, dummy, host, path = url.split('/', 3)
        except ValueError:
            proto, dummy, host = url.split('/', 2)
            path = ''
        if proto == 'http:':
            port = 80
        elif proto == 'https:':
            #import ussl
            port = 443
            ssl = True
        else:
            raise ValueError('Unsupported protocol: ' + proto)

        #if ':' in host:
        #    host, port = host.split(':', 1)
        #    port = int(port)
        #print("host", host)
        #print("port", port)

        '''ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
        if len(ai) < 1:
            raise ValueError('You are not connected to the internet...')
        ai = ai[0]
        #print(ai)
        s = usocket.socket(ai[0], ai[1], ai[2])'''


        #try:
        print(host)
        print(port)
        port = 80
        sock_reader, sock_writer = await asyncio.open_connection(host, port)
        #s.connect(ai[-1])
        #if proto == 'https:':
        #    s = ussl.wrap_socket(s, server_hostname=host)
        
        sock_writer.write(b'%s /%s HTTP/1.0\r\n' % (method, path))
        await sock_writer.drain()
        if not 'Host' in headers:
            sock_writer.write(b'Host: %s\r\n' % host)
            await sock_writer.drain()
        # Iterate over keys to avoid tuple alloc
        await self._write_headers(sock_writer, self._headers)
        await self._write_headers(sock_writer, headers)

        # add user agent
        sock_writer.write(b'User-Agent: MicroPython Client\r\n')
        await sock_writer.drain()
        if json is not None:
            assert data is None
            import ujson
            data = ujson.dumps(json)
            sock_writer.write(b'Content-Type: application/json\r\n')
            await sock_writer.drain()

        if data:
            sock_writer.write(b'Content-Length: %d\r\n' % len(data))
            await sock_writer.drain()
            sock_writer.write(b'\r\n')
            await sock_writer.drain()
            sock_writer.write(data)
            await sock_writer.drain()
        elif file:
            sock_writer.write(b'Content-Length: %d\r\n' % os.stat(file)[6])
            await sock_writer.drain()
            sock_writer.write(b'\r\n')
            await sock_writer.drain()
            with open(file, 'r') as file_object:
                for line in file_object:
                    sock_writer.write(line + '\n')
                    await sock_writer.drain()
        elif custom:
            custom(s)
        else:
            sock_writer.write(b'\r\n')
            await sock_writer.drain()

        l = await sock_reader.readline()
        # print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ''
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = await sock_reader.readline()
            if not l or l == b'\r\n':
                break
            # print(l)
            if l.startswith(b'Transfer-Encoding:'):
                if b'chunked' in l:
                    raise ValueError('Unsupported ' + l)
            elif l.startswith(b'Location:') and not 200 <= status <= 299:
                raise NotImplementedError('Redirects not yet supported')
        resp = Response(sock_reader, saveToFile)
        if saveToFile != None:
            await resp.save(saveToFile)
        else:
            await resp.copyToVariable()
        #await resp.save(sock_reader, saveToFile)
        #resp.data = await resp.text


        #except Exception as e:
        #    print("Except ", e)
            #s.close()
        #   raise
        #finally:
        #    s.close()

        sock_reader.close()
        await sock_reader.wait_closed()
        sock_writer.close()
        await sock_writer.wait_closed()

        resp.status_code = status
        resp.reason = reason
        return resp

    def head(self, url, **kw):
        return self.request('HEAD', url, **kw)

    def get(self, url, **kw):
        return self.request('GET', url, **kw)

    def post(self, url, **kw):
        return self.request('POST', url, **kw)

    def put(self, url, **kw):
        return self.request('PUT', url, **kw)

    def patch(self, url, **kw):
        return self.request('PATCH', url, **kw)

    def delete(self, url, **kw):
        return self.request('DELETE', url, **kw)


async def test_http():
    cli = HttpClient()
    #url = "https://smacsystem.com/smacapi/request_test"
    #url = "http://micropython.org"
    url = "http://smacsystem.com/download/esp32/version.json"
    resp = await cli.request("GET", url)
    print(resp.status_code)
    print(resp.data)

async def tt():
    await asyncio.sleep(1)
    while 1:
        await asyncio.sleep(1)

async def main():
    #t1 = asyncio.create_task( tt() )
    #t2 = asyncio.create_task( test_http() )
    #await t1
    #await t2
    await test_http()
    
    

#asyncio.run(main())