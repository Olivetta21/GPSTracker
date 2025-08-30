#include <iostream>
#include <vector>
#include <cstdint>
#include "Crypt.cpp"


void printBytes(const byte* data, byte size) {
    for (byte i = 0; i < size; i++) {
        std::cout << static_cast<int>(data[i]) << " ";
    }
    std::cout << std::endl;
}



bool testGens(Crypt& crypt) {
    byte data[BUFFER_SIZE] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09};
    byte dataSize = 9;
    byte enc[BUFFER_SIZE] = {0};
    byte dec[BUFFER_SIZE] = {0};

    memcpy(enc, data, dataSize);
    byte encryptedSize = crypt.encrypt(enc, dataSize);
    memcpy(dec, enc, encryptedSize);
    byte decryptedSize = crypt.decrypt(dec, encryptedSize);

    std::cout << "Encrypted data: ";
    printBytes(enc, encryptedSize);

    for (byte i = 0; i < dataSize; i++) {
        if (data[i] != dec[i]) {
            std::cout << "\n\n\nOriginal data: ";
            printBytes(data, dataSize);
            std::cout << "Encrypted data: ";
            printBytes(enc, encryptedSize);
            std::cout << "Decrypted data: ";
            printBytes(dec, decryptedSize);
            return false;
        }
    }
    return true;
}

int main()
{
    Crypt crypt;
    crypt.setKeys((byte[KEY_SIZE]) {0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF, 0x01});


    byte otherEncrypted[28] = {0};
    const int otherValues[] = {20, 135, 21, 177, 59, 90, 251, 190, 135, 77, 130, 23, 114, 252, 90, 207, 97, 22, 146, 176, 31, 246, 119, 47, 23, 32, 15, 235};
    for (byte i = 0; i < sizeof(otherEncrypted); i++) {
        otherEncrypted[i] = (byte) otherValues[i];
    }

    std::cout << "\nOther Encrypted data: ";
    printBytes(otherEncrypted, sizeof(otherEncrypted));
    byte decryptedSize = crypt.decrypt(otherEncrypted, sizeof(otherEncrypted));
    std::cout << "Other decrypted data: ";
    printBytes(otherEncrypted, decryptedSize);

    std::cout << "\n\n Iniciando testes:\n";

    for (byte i = 0; i < 20000; i++) {
        if (testGens(crypt)) {
            std::cout << ".";
        } else {
            std::cout << "\n\nfailed!";
            return 1;
        }
    }

    return 0;
}
