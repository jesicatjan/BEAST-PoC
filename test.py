import random
import binascii
import sys
from Crypto.Cipher import AES
from Crypto import Random

# def pad(s):
#     print("s len")
#     print(len(s))
#     padding_length = 16 - len(s) % 16
#     return repr(s + chr(padding_length) * padding_length)

# pad("password: ")

# print(pad("password: "))

def pad(s):
    # Calculate the padding length needed to make `s` a multiple of 16 bytes
    print("length of s: ", len(s))
    padding_length = 16 - (len(s) % 16)
    # Return the original string `s` with padding appended
    return s + (padding_length) * chr(padding_length)


def encrypt(msg, iv_p=None):
    print("encrypt message: ", msg)
    print("padded message: ", pad(msg))
    raw = pad(msg).encode()
    print("raw: ", raw)

    iv = iv_p if iv_p is not None else Random.new().read(AES.block_size)
    key = b'V38lKILOJmtpQMHp'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(raw)




first_r = encrypt("flag: 123_UrI@Lg")
print(first_r)
