from ctypes_ import UInt8 as byte
from random import randint

# Encryption config
KEY_SIZE = 16
IV_SIZE = 16
BUFFER_SIZE = 33
CHECKSUM_SIZE = 2
ROUNDS = 2
#

if IV_SIZE + CHECKSUM_SIZE >= BUFFER_SIZE:
    raise ValueError("buffer size too small")

class Crypt:
    
    def __init__(self):
        self.__keys = [[byte(0) for _ in range(KEY_SIZE)] for _ in range(ROUNDS)]

    def generateSubkeys(self) -> None:
        for i in range(1, ROUNDS):
            for j in range(KEY_SIZE):
                prevByte = self.__keys[i - 1][j]
                self.__keys[i][j] = ((prevByte << 3) | (prevByte >> 5)) ^ (j + i * 7)

    def encodeByte(self, byte_: byte, key: byte, mod: byte) -> byte:
        match mod:
            case 0:
                byte_ ^= key
            case 1:
                byte_ += key
            case _:
                byte_ = ((byte_ << 4) | (byte_ >> 4)) ^ key        
        return byte_

    def decodeByte(self, byte_: byte, key: byte, mod: byte) -> byte:
        match mod:
            case 0:
                byte_ ^= key
            case 1:
                byte_ -= key
            case _:
                tmp = byte_ ^ key
                byte_ = ((tmp >> 4) | (tmp << 4))
        return byte_
    
    def enc_dec_byteArray(self, byte_array: list[byte], round: int, encode: bool) -> None:
        for i in range(len(byte_array)):
            mod = (i + round) % 3
            key = self.__keys[round][i % KEY_SIZE]
            if encode:
                byte_array[i] = self.encodeByte(byte_array[i], key, mod)
            else:
                byte_array[i] = self.decodeByte(byte_array[i], key, mod)

    def genAndInsertIV(self, byte_array: list[byte]) -> bool:
        if (len(byte_array) + IV_SIZE + CHECKSUM_SIZE > BUFFER_SIZE):
            return False
        temp = byte_array.copy()
        byte_array += [None] * IV_SIZE
        byte_array[IV_SIZE:] = temp[:]
        for i in range(IV_SIZE):
            byte_array[i] = byte(randint(0, 255))
        return True
    
    def genAndInsertChecksum(self, byte_array: list[byte]) -> bool:
        if (len(byte_array) + CHECKSUM_SIZE > BUFFER_SIZE):
            return False
        checksum = 0
        for i in range(len(byte_array)):
            checksum += int(byte_array[i])
        for i in range(CHECKSUM_SIZE):
            byte_array.append(byte((checksum >> (8 * (CHECKSUM_SIZE - 1 - i))) & 0xFF))
        return True

    def de_ob_fuscateWithIV(self, byte_array: list[byte]) -> bool:
        if (len(byte_array) <= IV_SIZE):
            return False
        for i in range(IV_SIZE, len(byte_array)):
            byte_array[i] ^= byte_array[i % IV_SIZE]
        return True

    def testAndRemoveChecksum(self, byte_array: list[byte]) -> bool:
        constructedChecksum = 0
        for i in range(CHECKSUM_SIZE):
            constructedChecksum |= (int(byte_array[len(byte_array) - CHECKSUM_SIZE + i]) << (8 * (CHECKSUM_SIZE - 1 - i)))
        for i in range(len(byte_array) - CHECKSUM_SIZE):
            constructedChecksum -= int(byte_array[i])
        if constructedChecksum != 0:
            return False
        byte_array[:] = byte_array[:len(byte_array) - CHECKSUM_SIZE]
        return True

    def encrypt(self, byte_array: list[byte]) -> bool:
        if not self.genAndInsertIV(byte_array):
            return False
        if not self.genAndInsertChecksum(byte_array):
            return False
        if not self.de_ob_fuscateWithIV(byte_array):
            return False
        for round in range(ROUNDS):
            self.enc_dec_byteArray(byte_array, round, True)
        return True

    def decrypt(self, byte_array: list[byte]) -> bool:
        for round in range(ROUNDS - 1, -1, -1):
            self.enc_dec_byteArray(byte_array, round, False)
        if not self.de_ob_fuscateWithIV(byte_array):
            return False
        if not self.testAndRemoveChecksum(byte_array):
            return False
        if IV_SIZE >= len(byte_array):
            return False
        byte_array[:] = byte_array[IV_SIZE:]
        return True

    def setKeys(self, byte_array: list[byte]) -> None:
        self.__keys[0] = byte_array[:KEY_SIZE]
        self.generateSubkeys()
    
