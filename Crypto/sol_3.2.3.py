import sys
import urllib.request, urllib.error
from Crypto.Cipher import AES
from Crypto import Random

url =  'http://172.22.159.75:4000/mp3/yclai4/?'

def get_status(u):
    try:
        resp = urllib.request.urlopen(u)
        print(resp.read())
    except urllib.error.HTTPError as e:
        return e.code

def get_plain_text(iv, cipher_block, is_final_block):
    
    cipher_text = [int(cipher_block[i*2:i*2+2],16) for i in range(16)]
    iv = [int(iv[i*2:i*2+2],16) for i in range(16)]
    plain_pred = [0]*16
    padding_iv = [0]*16
    for idx in range(0xF, -1, -1):
        for i in range(idx, 0x10):
            padding_iv[i] = iv[i] ^ (0x10+idx-i)
        for guess in range(0x100):
            plain_pred[idx] = guess
            arg = ''.join('{:02x}'.format(padding_iv[i]^plain_pred[i]) for i in range(16))
            status = get_status(url + arg + cipher_block.decode("utf-8"))
            if status == 404:
                break
        
        # print('plain_pred = ', plain_pred)
        plain_pred[idx] = guess
    # print('||', ''.join(chr(pred) for pred in plain_pred), '||')
    if is_final_block:
        # print(plain_pred)
        pivot = -1
        for i in range(16):
            if pivot>-1 and plain_pred[i] != 16-i+pivot:
                pivot = -1
            if plain_pred[i] == 16:
                pivot = i
        if pivot>-1:
            plain_pred = plain_pred[:pivot]
        # print(plain_pred)
    return ''.join(chr(pred) for pred in plain_pred)


def main():
    msg = open(sys.argv[1], 'rb').read().strip()
    plain_text = ''
    cipher_block = [msg[i*32:(i+1)*32] for i in range(len(msg)//32)]
    for i in range(len(msg)//32-1):
        is_final_block = (i==len(msg)//32-2)
        plain_text_i = get_plain_text(cipher_block[i], cipher_block[i+1], is_final_block)
        plain_text += plain_text_i
        # print(plain_text_i)
    
    with open(sys.argv[2], 'w') as f:
        f.write(plain_text)
    print(plain_text)
if __name__ == '__main__':
    main()