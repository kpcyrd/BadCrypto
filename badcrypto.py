#!/usr/bin/env python
from hashlib import sha256
from argparse import ArgumentParser
import sys


class Crypto(object):
    def __init__(self, password):
        self.state = sha256(password)

    def crypt(self, chunk, encrypt):
        chunk = bytearray(chunk)
        for i, x in enumerate(chunk):
            k = self.state.digest()[0]
            c = x ^ ord(k)
            self.state.update(chr(x if encrypt else c))
            chunk[i] = c

        return str(chunk)

    def encrypt(self, chunk):
        return self.crypt(chunk, True)

    def decrypt(self, chunk):
        return self.crypt(chunk, False)

parser = ArgumentParser()


def main():
    parser.add_argument('action', choices=['encrypt', 'decrypt'])
    parser.add_argument('psk')

    args = parser.parse_args()

    c = Crypto(args.psk)

    while True:
        x = sys.stdin.read(1024)
        if len(x) == 0:
            break
        x = getattr(c, args.action)(x)
        sys.stdout.write(x)


if __name__ == '__main__':
    main()
