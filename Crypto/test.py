with open('3.1.1_value.hex') as f:
    a = f.read().strip()

print((int(a, 16)))
print(bin((int(a, 16))))