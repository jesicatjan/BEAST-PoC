#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    BEAST attack - PoC
    Implementation of the cryptographic path behind the attack
    Author: mpgn <martial.puygrenier@gmail.com>
'''

import random
import binascii
import sys
from Crypto.Cipher import AES
from Crypto import Random

# Padding and unpadding functions for AES block size of 16 bytes
def pad(s):
    print("length of s: ", len(s))
    padding_length = 16 - (len(s) % 16)
    return s + (padding_length) * chr(padding_length)

def unpad(s):
    return s[:-ord(s[-1:])]

# Encrypt function simulating TLS 1.0's fixed IV issue
def encrypt(msg, iv_p=None):
    print("encrypt message: ", msg)
    print("padded message: ", pad(msg))

    raw = pad(msg).encode()
    print("raw: ", raw)

    iv = iv_p if iv_p is not None else Random.new().read(AES.block_size)
    key = b'V38lKILOJmtpQMHp'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(raw)

# XOR utility functions
def xor_strings(xs, ys, zs):
    return "".join(chr(x ^ y ^ z) for x, y, z in zip(xs, ys, zs))

def xor_block(vector_init, previous_cipher, p_guess):
    return xor_strings(vector_init, previous_cipher, p_guess)

def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

# Run the BEAST attack simulation using two requests
def run_two_request(find_me):
    print("Start decrypting the request block 0 --> block 0\n")
    
    secret = []
    i_know = "flag: "
    padding = 16 - len(i_know) - 1
    i_know = "a" * padding + i_know
    add_byte = 16
    length_block = 16
    t = 0

    while t < (len(find_me) - len("flag: ")):
        for i in range(256):
            s = find_me if (add_byte + padding) >= 0 else find_me[-(add_byte + padding):]
            print("EE")
            print(s)
            string_enc = "a" * (add_byte + padding) + s
            print(string_enc)
            print("FF")
            enc = encrypt("a" * (add_byte + padding) + s)
            print(enc)
            print("GG")
            original = split_len(binascii.hexlify(enc).decode(), 32)

            vector_init = enc[-length_block:]
            previous_cipher = enc[:length_block]
            p_guess = (i_know + chr(i)).encode()
            
            xored = xor_block(vector_init, previous_cipher, p_guess)
            enc = encrypt(xored, vector_init)
            result = split_len(binascii.hexlify(enc).decode(), 32)

            sys.stdout.write(f"\r{original[1]} -> {result[0]}")
            sys.stdout.flush()

            if result[0] == original[1]:
                print(f" Find char {chr(i)}")
                i_know = i_know[1:] + chr(i)
                add_byte -= 1
                secret.append(chr(i))
                t += 1
                break
            elif i == 255:
                print("Unable to find the char...")
                return secret
    return secret

# Run the BEAST attack simulation using three requests
def run_three_request(find_me):
    print("Start decrypting the request using block 0 --> block 1\n")

    secret = []
    i_know = "flag: "
    padding = 16 - len(i_know) - 1
    i_know = "a" * padding + i_know
    length_block = 16
    t = 0

    while t < (len(find_me) - len("flag: ")):
        for i in range(256):
            s = find_me if padding >= 0 else find_me[-padding:]
            print("padding: ", padding)
            print("find_me[-padding:]: ", find_me[-padding:])
            
            first_r = encrypt("a"*(padding) + s)
            print("first_r: ", first_r)
            print("first_r[-length_block:]: ", first_r[-length_block:])

            enc = encrypt("a" * padding + s, first_r[-length_block:])
            print("enc: ", enc)


            original = split_len(binascii.hexlify(enc).decode(), 32)

            vector_init = enc[-length_block:]
            previous_cipher = first_r[-length_block:]
            p_guess = (i_know + chr(i)).encode()
            
            xored = xor_block(vector_init, previous_cipher, p_guess)
            enc = encrypt(xored, vector_init)
            result = split_len(binascii.hexlify(enc).decode(), 32)

            sys.stdout.write(f"\r{original[0]} -> {result[0]}")
            sys.stdout.flush()

            if result[0] == original[0]:
                print(f" Find char {chr(i)}")
                i_know = i_know[1:] + chr(i)
                padding -= 1
                secret.append(chr(i))
                t += 1
                break
            elif i == 255:
                print("Unable to find the char...")
                return secret
    return secret

# Attempt to retrieve the flag using the BEAST attack
secret = run_three_request("flag: 123_UrI@L")
found = ''.join(secret)
print("\n" + found)
