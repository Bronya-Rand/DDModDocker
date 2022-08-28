
import hashlib

print(hashlib.sha256(open("scripts.rpa", "rb").read()).hexdigest())