import sys

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        ciphertext = f.read().strip()
    with open(sys.argv[2]) as f:
        sub_key = f.read().strip()
    for ind, sub_char in enumerate(sub_key):
        ciphertext = ciphertext.replace(sub_char, chr(ord('a')+ind))

    f = open(sys.argv[3], "w")
    f.write(ciphertext.upper())
    f.close()
