import hashlib

h1 = hashlib.sha1()
h2 = hashlib.sha1()

h1.update('H'.encode('utf-8'))
h2.update('H '.encode('latin-1'))

print(h1.hexdigest())
print(h2.hexdigest())