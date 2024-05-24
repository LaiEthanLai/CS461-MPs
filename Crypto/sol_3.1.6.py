import sys

with open(sys.argv[1], 'r') as f:
    in_str_chr = f.read().strip()

out_file = open(sys.argv[2], 'w')

# hashing
mask = 0x3fffffff
out = 0
for i in in_str_chr:
    ascii_num = ord(i)
    intermediate_value = ((ascii_num ^ 0xcc) << 24) | \
        ((ascii_num ^ 0x33) << 16) | \
        ((ascii_num ^ 0xaa) << 8) | \
        ascii_num ^ 0x55
    out = (out & mask) + (intermediate_value & mask)

out = format(out, '08x')
print(out)
out_file.write(out)
