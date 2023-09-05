import asyncio, sys, ssl

LISTEN_PORT = 7500
#DST_PORT = 26257
#DST_HOST = "acadia-uni-4762.g8z.cockroachlabs.cloud"

DST_PORT = 443
DST_HOST = "wikipedia.com"
#DST_HOST = "neverssl.com"

# TODO: How do I account for the ?sslmode=verify-full
# TODO: How do I specify that the connection to the server is TLS at all? 
# Will I need to handle this differently between tests and the actual connection to CockroachDB?

# setup local root cert for CDB
# certs, other parameters can be passed to open_connection() using an ssl context

# check whether CockroachDB supports LISTEN/NOTIFY (also, figure out what that even is)

# FIXME: Get GPT-4 to generate textbook quality explanation of implementing TLS on this code example
# pass in 
# - this code
# - python asyncio docs - everything that even might be relevant
# - the ssl package docs - everything that even might be relevant
# - the source code for the relevant sections of both the asyncio and ssl packages

async def pipe(reader, writer):
    try:
        while not reader.at_eof():
            data = await reader.read(2048)
            print(f"Received {data!r}")
            writer.write(data)
    finally:
        writer.close()

async def handle_client(client_reader, client_writer):
    try:
        # connect to database server
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = True
        server_reader, server_writer = await asyncio.open_connection(
            DST_HOST, DST_PORT, ssl=ssl_context)
        print("Connected to server")
        pipe1 = pipe(client_reader, server_writer)
        pipe2 = pipe(server_reader, client_writer)
        await asyncio.gather(pipe1, pipe2)
    except Exception as e:
        # printing the error message
        print(f"Error connecting to server: {sys.exc_info()[0]}")
        print(f"{e}")
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
    await server.wait_closed()

asyncio.run(main())