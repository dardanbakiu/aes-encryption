from AESencrypt import encrypt
from AESdecrypt import decrypt
import random
import string

msg = 'hello world'
key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
key = '1234567890123456'

encmsg = encrypt(msg, key)
# print(encmsg)

decmsng = decrypt(key, encmsg)
print(decmsng)


name = 'dardan'

# welcome = 'Pershendetje #ENC_DEC_PARTIALLY%s#ENC_DEC_PARTIALLY! shkruaj {quit} qe te dilni nga chati.' % name
# welcome = welcome.split("#ENC_DEC_PARTIALLY")
# welcome[1] = encrypt(welcome[1], key)

# print(welcome)
# welcome[1] = decrypt(key, welcome[1]) #qet kod se qet