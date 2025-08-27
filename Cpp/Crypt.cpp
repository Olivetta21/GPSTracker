#include <iostream>
#include <stdint.h>

// Unsigned 8 bits
typedef uint8_t byte;

//#define ISARDUINO
#define ISDEBUG

// Put variables in flash if arduino
#ifdef ISARDUINO
    #define print(msg) Serial.println(msg)
#else
    #define print(msg) std::cout << msg << std::endl
    #define F(msg) msg
    #define PROGMEM
#endif


#define KEY_SIZE 16
#define IV_SIZE 4
#define BUFFER_SIZE 64
#define CHECKSUM_SIZE 2

class Crypt {
    private:
    byte key[KEY_SIZE];

    /**
     * @brief Encrypt or decrypt a single byte.
     * @param byte Byte to encrypt or decrypt.
     * @return The encrypted or decrypted byte.
     * @note This function does not care about the result. Good luck!
     *
     */
    byte enc_dec_byte(byte byte);

    /**
     * @brief Generate and insert an IV in the beginning of the array.
     * @param data Pointer to the array to be inserted into.
     * @param size Size of the array.
     * @return The new size of the data including the IV, Zero if failed.
     *
     */
    byte genAndInsertIV(byte* data, byte size);

    /**
     * @brief Generate and insert a checksum at the end of the array.
     * @param data Pointer to the array to be inserted into.
     * @param size Size of the array.
     * @return The new size of the data including the checksum, Zero if failed.
     *
     */
    byte genAndInsertChecksum(byte* data, byte size);

    /**
     * @brief Test and remove the checksum from the data.
     * @param data Pointer to the array to be tested.
     * @param size Size of the array.
     * @return The new size of the data excluding the checksum, Zero if failed.
     *
     */
    byte testAndRemoveChecksum(byte* data, byte size);

    public:

    /**
     * @brief Create Crypt object.
     * @param key Pointer to key array.
     * @param size Size of the key array.
     *
     */
    Crypt(const byte* key, const byte size);

    /**
     *  @brief Encrypt the given data.
     *  @param data Pointer to the array to be encrypted.
     *  @param size Size of the array.
     *  @return The size of the encrypted data. Zero if failed.
     *
     */
    byte encrypt(byte* data, byte size);

    /**
     *  @brief Decrypt the given data.
     *  @param data Pointer to the array to be decrypted.
     *  @param size Size of the array.
     *  @return The size of the decrypted data. Zero if failed.
     *
     */
    byte decrypt(byte* data, byte size);
};

byte Crypt::enc_dec_byte(byte byte) {
    byte ^= key[0];
    return byte;
}

byte Crypt::genAndInsertIV(byte* data, byte size) {
    if (size + IV_SIZE + CHECKSUM_SIZE > BUFFER_SIZE) {
        return 0;
    }
    byte temp[size];
    memcpy(temp, data, size);
    memcpy(data + IV_SIZE, temp, size);

    for (byte i = 0; i < IV_SIZE; i++) {
        data[i] = (byte) (std::rand() % 255);
    }

    return size + IV_SIZE;
}

byte Crypt::genAndInsertChecksum(byte* data, byte size) {
    if (size + CHECKSUM_SIZE > BUFFER_SIZE) {
        return 0;
    }
    uint16_t checksum = 0;
    if (sizeof(checksum) / sizeof(byte) != CHECKSUM_SIZE) {
        return 0;
    }
    for (byte i = 0; i < size; i++) {
        checksum += data[i];
    }

    byte nibbles[CHECKSUM_SIZE] = {0};
    for (byte i = 0; i < CHECKSUM_SIZE; i++) {
        nibbles[i] = (checksum >> (8 * (CHECKSUM_SIZE - 1 - i))) & 0xFF;
        data[size + i] = nibbles[i];
    }

    return size + CHECKSUM_SIZE;
}

byte Crypt::testAndRemoveChecksum(byte* data, byte size) {
    uint16_t constructedChecksum = 0;
    if (sizeof(constructedChecksum) / sizeof(byte) != CHECKSUM_SIZE) {
        return 0;
    }
    for (byte i = 0; i < CHECKSUM_SIZE; i++) {
        constructedChecksum |= (static_cast<uint16_t>(data[size - CHECKSUM_SIZE + i]) << (8 * (CHECKSUM_SIZE - 1 - i)));
    }
    
    for (byte i = 0; i < size - CHECKSUM_SIZE; i++) {
        constructedChecksum -= data[i];
    }

    if (constructedChecksum != 0) {
        return 0;
    }

    return size - CHECKSUM_SIZE;
}

Crypt::Crypt(const byte* key, const byte size) {
    #ifdef ISDEBUG
        if (size != KEY_SIZE) {
            print(F("Wrong key size"));
        }
    #endif
    memcpy(this->key, key, KEY_SIZE);
}

byte Crypt::encrypt(byte* data, byte size) {
    size = genAndInsertIV(data, size);
    size = genAndInsertChecksum(data, size);
    for (byte i = 0; i < size; i++){
        data[i] = enc_dec_byte(data[i]);
    }
    return size;
}

byte Crypt::decrypt(byte* data, byte size) {
    for (byte i = 0; i < size; i++){
        data[i] = enc_dec_byte(data[i]);
    }
    size = testAndRemoveChecksum(data, size);
    memcpy(data, data + IV_SIZE, size);

    return size - IV_SIZE;
}












void printBytes(const byte* data, byte size) {
    for (byte i = 0; i < size; i++) {
        std::cout << static_cast<int>(data[i]) << " ";
    }
    std::cout << std::endl;
}

int main()
{
    const byte masterKey[] PROGMEM = {0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01};
    Crypt crypt(masterKey, sizeof(masterKey));

    byte data[BUFFER_SIZE] = {0x01, 0x04, 0xFF, 0x01, 0x04, 0xFF,0x01, 0x04, 0xFF};
    byte dataSize = 9;
    std::cout << "Original data: ";
    printBytes(data, dataSize);

    byte encryptedSize = crypt.encrypt(data, dataSize);
    std::cout << "Encrypted data: ";
    printBytes(data, encryptedSize);

    byte decryptedSize = crypt.decrypt(data, encryptedSize);
    std::cout << "Decrypted data: ";
    printBytes(data, decryptedSize);

    return 0;
}
