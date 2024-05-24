import sys

# open files and load necessary stuff
with open(sys.argv[1], 'r') as f:
    cipher_text = f.read().strip()
    cipher_text_int = int(cipher_text, 16)

with open(sys.argv[2], 'r') as f:
    key = f.read().strip()
    key_int = int(key, 16)

with open(sys.argv[3], 'r') as f:
    mod = f.read().strip()
    mod_int = int(mod, 16)

out_file = open(sys.argv[4], 'w') 
    
# decryption
out_file.write(hex(pow(cipher_text_int, key_int, mod_int))[2:])