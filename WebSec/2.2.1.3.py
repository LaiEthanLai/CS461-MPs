from hashlib import md5
import random, re

unhashed = ""
while(re.search(r"'='.+", str(md5(unhashed.encode()).digest())) is None):
    unhashed = ""
    for i in range(0,3):
        unhashed += str(random.randint(0, 2**30))
   
print(unhashed)
print(md5(unhashed.encode()).digest())
