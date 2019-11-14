import socket
from time import sleep
from select import select
import asyncio

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8700))
s.listen(5)
s.setblocking(False)


async def client_handler(client, client_info):
    print('Got connection from {}:{}'.format(*client_info))
    data = None
    while data != b'q':
        data = (await loop.sock_recv(client, 1024))
        response = 'Got {}'.format(data)
        await loop.sock_sendall(client, response.encode('utf-8'))

async def run_server(server):
    i = 0
    while i < 10:
        client, client_info = await loop.sock_accept(server)
        loop.create_task(client_handler(client, client_info))
        i += 1



loop = asyncio.get_event_loop()
loop.run_until_complete(run_server(s))
