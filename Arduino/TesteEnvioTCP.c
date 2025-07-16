struct Pacote {
    float latitude;
    float longitude;
    char token[10];
    uint8_t msg_id;
} __attribute__((packed)); // sem padding

void setup() {
    if (client.connect(server_ip, server_port)) {
        Serial.println("Conectado ao servidor");

        Pacote pacote;
        pacote.latitude = 12.345678;
        pacote.longitude = -45.123456;
        strncpy(pacote.token, "arduino_01", 10);
        pacote.msg_id = 1;

        client.write((uint8_t*)&pacote, sizeof(Pacote));
    }
}
