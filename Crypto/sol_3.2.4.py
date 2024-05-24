from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
from pbp import decrypt
from math import gcd, ceil, floor
from argparse import ArgumentParser
from time import time

# reference: https://facthacks.cr.yp.to/index.html and https://factorable.net/weakkeys12.extended.pdf 
def product(x: list) -> int:

    return x[0]*x[1] if len(x) == 2 else x[0]

def product_tree(x: list) -> list:

    out_lists = [x]
    print('constructing the product tree')
    s = time()
    while len(x) > 1:
        x = [product(x[2*i:2*(i+1)]) for i in (range(ceil(len(x)/2)))]
        out_lists.append(x)
    print(f'done, takes {time()-s} seconds')
    return out_lists

def remainder_tree(x: list) -> list:

    out_lists = [x[-1][0]]
    print('constructing the remainder tree')
    s = time()
    for i in range(len(x)-2, -1, -1):
        out_lists = [out_lists[floor(j/2)] % (x[i][j]**2) for j in range(len(x[i]))]
    print(f'done, takes {time()-s} seconds')
    return out_lists

def test(len: int) -> None:

    from random import random

    xx  = [int(random()*100)+1 for i in range(len)]

    a = time()
    c1 = product_tree(xx)
    c2 = remainder_tree(c1)
    out = []
    for idx, i in enumerate(c2):
        out += gcd((i // xx[idx] ), xx[idx]),

    print(time()-a)

    print('---------')

    aa = time()
    outt = 1
    for i in xx:
        outt *= i

    a = []
    for i in xx:
        a += gcd((outt % (i**2)) // i, i),

    print(time()-aa)
    print(a==out)

def main(args):

    if args.debug:
        test(args.len)
        return

    mod_list = []
    with open(args.mod, 'r') as f:
        for line in f:
            mod_list += int(line, 16),

    products = product_tree(mod_list)
    remainders = remainder_tree(products)

    Ps = []
    valid_mod = []
    print('computing GCDs')
    for idx, i in enumerate(remainders):
        p = gcd((i // mod_list[idx]), mod_list[idx])
        if p != 1:
            Ps += p,
            valid_mod += mod_list[idx],

    print('done')

    print(valid_mod)

    with open(args.cipher, 'r') as f:
        ciphertext = f.read()

    for i in range(len(valid_mod)):

        p = Ps[i]
        modulus = valid_mod[i]
        q = modulus // p
        d = inverse(65537, (p-1)*(q-1))
        # Construct the RSA key for the computed values
        key = RSA.construct((int(modulus), int(65537), int(d)))
        try:
            plaintext = decrypt(key, ciphertext) 
            print(plaintext.decode('ascii'))
            with open(args.output, 'w') as out_file:
                out_file.write(plaintext.decode('ascii'))
                print(f'Written to {args.output}!')
        except ValueError:
            pass
    
    return

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--len', type=int, default=10000)
    parser.add_argument('--cipher', type=str, default='3.2.4_ciphertext.enc.asc')
    parser.add_argument('--mod', type=str, default='moduli.hex')
    parser.add_argument('--output', type=str, default='sol_3.2.4.txt')
    main(parser.parse_args())