#!/usr/bin/env python
from __future__ import print_function
from hashlib import sha256
import sys

class Crypto(object):
	def __init__(self, password):
		self.state = sha256(password)

	def crypt(self, chunk):
		chunk = bytearray(chunk)
		for i, x in enumerate(chunk):
			k = self.state.digest()[0]
			c = x ^ ord(k)
			self.state.update(chr(x ^ c))
			chunk[i] = c

		return str(chunk)


def main():
	if len(sys.argv) == 1:
		usage = 'Usage: %s <shared secret>' % sys.argv[0]
		print(usage, file=sys.stderr)
		return

	c = Crypto(sys.argv[1])

	while True:
		x = sys.stdin.read(1024)
		if len(x) == 0:
			break
		x = c.crypt(x)
		sys.stdout.write(x)


if __name__ == '__main__':
	main()
