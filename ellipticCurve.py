import math
import os
import random
import imgToDat
import numpy as np


def read_inverse(filename):
    f1 = open(filename, "r")
    inver = f1.read()
    inver = inver[1:len(inver) - 1].split(', ')
    f1.close()
    return inver


def calc_inverse(prime, filename):
    inv = [0] * prime
    inv[1] = 1
    for i in range(2, prime):
        inv[i] = (prime - prime // i) * inv[prime % i] % prime
    f2 = open(filename, 'w')
    f2.write(str(inv))
    f2.close()


class Elliptic:

    def __init__(self, prime, aa, bb, file_name, xg=None, yg=None):
        self.p = prime
        self.a = aa
        self.b = bb
        if xg is None and yg is None:
            self.xGround, self.yGround = Elliptic.find_first_feasible(self)
        else:
            self.xGround, self.yGround = xg, yg
        self.inverse = read_inverse(file_name)
        self.n = 1
        self.priv_key = 2
        self.public_key = None

    def get_inverse(self, value):
        if value >= len(self.inverse):
            return Elliptic.get_inverse_complex(self, value)
        return int(self.inverse[value])

    def get_inverse_complex(self, value):
        for i in range(1, self.p):
            if (i * value) % self.p == 1:
                return i
        return -1

    def step(self, x1, y1, x2, y2):
        neg = 0
        if x1 == x2 and y1 == y2:
            mem = 3 * (x1 ** 2) + self.a
            denom = 2 * y1
        else:
            mem = y2 - y1
            denom = x2 - x1
            if mem * denom < 0:
                neg = 1
                mem = abs(mem)
                denom = abs(denom)

        factor = math.gcd(mem, denom)
        mem = mem // factor
        denom = denom // factor
        denom_inverse = Elliptic.get_inverse(self, denom)
        if neg == 1:
            k = ((-1) * mem * denom_inverse) % self.p
        else:
            k = (mem * denom_inverse) % self.p

        x3 = (k ** 2 - x1 - x2) % self.p
        y3 = (k * (x1 - x3) - y1) % self.p
        return x3, y3

    def get_n(self):
        neg_x1 = self.xGround
        neg_y1 = (-1 * self.yGround) % self.p
        temp_x = self.xGround
        temp_y = self.yGround
        while self.n:
            self.n += 1
            temp_x, temp_y = Elliptic.step(self, temp_x, temp_y, self.xGround, self.yGround)
            if temp_x == neg_x1 and temp_y == neg_y1:
                self.n += 1
                break

    def get_dot(self, x0):
        y_expect = (x0 ** 3 + self.a * x0 + self.b) % self.p
        for i in range(self.p):
            if i ** 2 % self.p == y_expect:
                y0 = i
                x1 = x0
                y1 = (-1 * i) % self.p
                return x0, y0, x1, y1

    def get_ng(self, xg, yg, priv_key):
        end_x = xg
        end_y = yg
        for _ in range(priv_key):
            end_x, end_y = Elliptic.step(self, end_x, end_y, xg, yg)
        return end_x, end_y

    def get_key(self):

        Elliptic.get_n(self)
        # input('key length(<%d)：' % self.n)
        self.priv_key = 61
        xk, yk = Elliptic.get_ng(self, self.xGround, self.yGround, self.priv_key)
        self.public_key = (xk, yk)

    def encrypt2(self, plain):

        output = []
        # print('Encrypting：')
        for char in plain:
            intchar = int(char)
            r = random.randint(2, self.n // 2)
            kGx, kGy = Elliptic.get_ng(self, self.xGround, self.yGround, r)  # kG
            kQx, kQy = Elliptic.get_ng(self, self.public_key[0], self.public_key[1], r)  # kQ
            cipher = intchar * kQx
            output.append([kGx, kGy, cipher])
        # f3 = open("encrypt.txt", 'w')
        # f3.write(' '.join([str(x) for x in output]))
        # f3.close()
        return output

    def decrypt2(self, code):
        decipher = []
        for charArr in code:
            kQx, kQy = Elliptic.get_ng(self, charArr[0], charArr[1], self.priv_key)
            if kQx < 1e-8:
                decipher.append(np.uint8(charArr[2] * 1000))
            else:
                decipher.append(np.uint8(charArr[2] // kQx))
        return decipher

    def find_first_feasible(self):
        for i in range(self.p):
            v = Elliptic.get_dot(self, i)
            if v is not None:
                x0, y0, x1, y1 = v
                return x0, y0


def encrypt_to_disk(name):
    p = 487
    # p = 997
    a = 0
    b = 3

    document = "inverse_p" + str(p) + ".txt"
    if not os.path.exists(document):
        calc_inverse(p, document)
    ECC = Elliptic(p, a, b, document)

    ECC.get_key()
    # name = input("enter the file path and name: ")
    plain = imgToDat.compressedImg(name)
    return ECC.encrypt2(plain)#, plain


def decrypt_to_pic(c):
    p = 487
    # p = 997
    a = 0
    b = 3

    document = "inverse_p" + str(p) + ".txt"
    if not os.path.exists(document):
        calc_inverse(p, document)
    ECC = Elliptic(p, a, b, document)

    ECC.get_key()
    de = ECC.decrypt2(c)
    return de


############################################################
# # # testing code
# if __name__ == '__main__':
#     encrypt, plain = encrypt_to_disk("./img/space.jpg")
#     de = decrypt_to_pic(encrypt)
#     # print(encrypt)
#     ff = open("tttt.txt", 'w')
#     ff.write(str(de))
#     ff.close()
#     imgToDat.restoreImg(de, "trial.png")
#
#     if len(plain) == len(de):
#         print("same length")
#         for j in range(len(plain)):
#             if plain[j] != int(de[j]):
#                 print(plain[j], end=' ')
#             if max(encrypt[j]) > 131000:
#                 print(encrypt[j])
#         print()
#     else:
#         print("no equal length")
