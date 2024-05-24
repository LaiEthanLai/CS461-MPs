from pymd5 import md5, padding

pwd = b'eglcjdpf'
q = 'user=isflvksfan&command1=sdivsdpviaha&command2=dlkngfelkbn&command3=fafsflknfsba'
q_bytes = bytes(q, 'ascii')
extend_command = b'&command3=DeleteAllFiles'

h = md5()
h.update(pwd + q_bytes)

hh = md5()
hh.update(b'8940f24b3afff0a44b8547b12ea637b7' + padding(512) + extend_command)

print('original:')
print(h.hexdigest())

print('GT:')
print(hh.hexdigest())

