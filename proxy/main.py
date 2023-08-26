import asyncio
import sys

LISTEN_PORT = 7500
#DST_PORT = 26257
#DST_HOST = "acadia-uni-4762.g8z.cockroachlabs.cloud"

DST_PORT = 443
DST_HOST = "www.apache.org"

# TODO: How do I account for the ?sslmode=verify-full
# TODO: How do I specify that the connection to the server is TLS at all? 
# Will I need to handle this differently between tests and the actual connection to CockroachDB?

# setup local root cert for CDB
# certs, other parameters can be passed to open_connection() using an ssl context

# check whether CockroachDB supports LISTEN/NOTIFY (also, figure out what that even is)

async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            writer.write(await reader.read(2048))
    finally:
        writer.close()

async def handle_client(client_reader, client_writer):
    try:
        # connect to database server
        server_reader, server_writer = await asyncio.open_connection(
            DST_HOST, DST_PORT)
        print("Connected to server")
        pipe1 = pipe(client_reader, server_writer)
        pipe2 = pipe(server_reader, client_writer)
        await asyncio.gather(pipe1, pipe2)
    except:
        # printing the error message
        print(f"Error connecting to server: {sys.exc_info()[0]}")
    finally:
        print("Closing connection")
        client_writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', LISTEN_PORT)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.close()

asyncio.run(main())