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

class Crypt {
    private:
    byte key[KEY_SIZE];

    /**
     * @brief Encrypt or decrypt a single byte.
     * @param byte Reference to the byte to encrypt or decrypt.
     * @return True if successful, false otherwise.
     */
    bool enc_dec_byte(byte& byte);

    public:

    /**
     * @brief Create Crypt object.
     * @param key Pointer to a byte array.
     * @param size Size of the byte array.
     */
    Crypt(const byte* key, const byte size);

    /**
     *  @brief Encrypt the given data.
     *  @param data Array pointer to copy value into.
     *  @param size Size of the array.
     *  @return The size of the encrypted data. Or Zero if encryption failed.
     *
     */
    byte encrypt(byte* data, byte size);

    /**
     *  @brief Decrypt the given data.
     *  @param data Array pointer to copy value into.
     *  @param size Size of the array.
     *  @return The size of the decrypted data. Or Zero if decryption failed.
     *
     */
    byte decrypt(byte* data, byte size);
};

bool Crypt::enc_dec_byte(byte& byte) {
    byte ^= key[0];
    return true;
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
    for (byte i = 0; i < size; i++){
        if (!enc_dec_byte(data[i])) {
            return 0;
        }
    }
    return size;
}

byte Crypt::decrypt(byte* data, byte size) {
    for (byte i = 0; i < size; i++){
        if (!enc_dec_byte(data[i])) {
            return 0;
        }
    }
    return size;
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
    std::cout << "Size: " << sizeof(masterKey) << std::endl;
    Crypt crypt(masterKey, sizeof(masterKey));

    byte data[] = {0x01, 0x02, 0x03, 0x04};
    std::cout << "Original data: ";
    printBytes(data, sizeof(data));

    crypt.encrypt(data, sizeof(data));
    std::cout << "Encrypted data: ";
    printBytes(data, sizeof(data));

    crypt.decrypt(data, sizeof(data));
    std::cout << "Decrypted data: ";
    printBytes(data, sizeof(data));

    return 0;
}
