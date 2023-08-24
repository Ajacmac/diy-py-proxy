import asyncio

LISTEN_PORT = 7500
#DST_PORT = 26257
#DST_HOST = "acadia-uni-4762.g8z.cockroachlabs.cloud"

DST_PORT = 443
DST_HOST = "www.apache.org"

# TODO: How do I account for the ?sslmode=verify-full
# TODO: How do I specify that the connection to the server is TLS at all? 
# Will I need to handle this differently between tests and the actual connectino to CockroachDB?

async def handle_client(client_reader, client_writer):
    # read data from client
    data = await client_reader.read(100)
    print(f"Received {data.decode()!r}")

    # connect to database server
    server_reader, server_writer = await asyncio.open_connection(
        DST_HOST, DST_PORT, ssl=True)

    print('Sending to server...')
    server_writer.write(data)
    await server_writer.drain()

    data = await server_reader.read(100)
    print(f'Received: {data.decode()!r}')

    # pass data back to client
    client_writer.write(data)
    await client_writer.drain()

    # close connections
    print('Close the connection')
    server_writer.close()
    await server_writer.wait_closed()

    client_writer.close()
    await client_writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', LISTEN_PORT)

    async with server:
        await server.serve_forever()

asyncio.run(main())