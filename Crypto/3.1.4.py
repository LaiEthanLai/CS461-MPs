from Crypto.Cipher import AES
# from Crypto.Util.Padding import pad

# read cipher text
with open('3.1.4_aes_weak_ciphertext.hex') as f:
    cipher_text = f.read().strip()
cipher_text = bytes.fromhex(cipher_text)

# create iv and 251 bits of key
init_vec_byte = bytes.fromhex('0'*32) # 16 bytes
key_62 = '0'*62

# start guessing

# cipher_text = pad(cipher_text, 16)
for i in range(32):
    key = key_62 + format(i, '02x')
    print(f'key: {key}')
    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, IV=init_vec_byte)
    plain = cipher.decrypt(cipher_text)
    print(plain,'\n')