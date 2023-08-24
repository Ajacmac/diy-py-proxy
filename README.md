James Oakley recommended I use stream
https://docs.python.org/3/library/asyncio-stream.html


also available:
https://docs.python.org/3/library/socket.html


Notes:

I'm going to need to be very careful with testing this.
- Proxies probably have potential for weird and technical behaviour
- I'll need tests, and I'll need those tests to be good

Good project to learn TDD with

# TODO

- [x] setup basic cockroachdb or postgresql database example
- [ ] copy code for very basic passthrough proxy
- [ ] change example app to use proxy
- [ ] wireshark the connection to see if it it's encrypted
- [ ] try proxy with Brahms