from Crypt import Crypt
from ctypes_ import UInt8 as byte

arr = [byte(1),byte(2),byte(3),byte(4),byte(5),byte(6),byte(7),byte(8),byte(9),byte(10)]
cr = Crypt()

key = [0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01]
for i in range(len(key)):
    key[i] = byte(key[i])
cr.setKeys(key)

print("Before: ",arr)
cr.encrypt(arr)
print("Encrypted: ",arr)
cr.decrypt(arr)
print("Decrypted: ",arr)



encr = [104, 141, 136, 254, 253, 128, 196, 9, 14, 27, 1, 153, 92, 230, 172, 178, 166, 28, 235, 173, 93, 155, 232, 121, 175, 5, 188]
for i in range(len(encr)):
    encr[i] = byte(encr[i])

res = cr.decrypt(encr)
print("Other Decrypted: ", encr if res else "Failed")