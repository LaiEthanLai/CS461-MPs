import sys
from Crypto.Cipher import AES

# open files and load necessary stuff
with open(sys.argv[1], 'r') as f:
    cipher_text = f.read().strip()
    cipher_text_bytes = bytes.fromhex(cipher_text)
with open(sys.argv[2], 'r') as f:
    key = f.read().strip()
    key_bytes = bytes.fromhex(key)
with open(sys.argv[3], 'r') as f:
    init_vec = f.read().strip()
    iv_bytes = bytes.fromhex(init_vec)

out_file = open(sys.argv[4], 'w')

# decipher
cipher = AES.new(key_bytes, AES.MODE_CBC, IV=iv_bytes)
plaintext = cipher.decrypt(cipher_text_bytes)

out_file.writelines(plaintext.decode('utf-8').strip())