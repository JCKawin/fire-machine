// #include <WiFi.h>
// #include <WebServer.h>
//
// // Replace with your actual network credentials
// const char* ssid = "JCKAWIN";
// const char* password = "12345678";
//
// // Start the web server on port 80 (HTTP standard)
// WebServer server(80);
//
// // Your HTML page, stored inside raw literal string R"=====( ... )====="
// const char HTML_CONTENT[] PROGMEM = R"=====(
// <!DOCTYPE html>
// <html lang="en">
// <head>
//     <meta charset="UTF-8">
//     <meta name="viewport" content="width=device-width, initial-scale=1.0">
//     <title>ESP32-S3 Web Server</title>
//     <style>
//         body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
//         h1 { color: #333; }
//         p { color: #666; font-size: 1.2rem; }
//         .card { background: white; padding: 20px; display: inline-block; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
//     </style>
// </head>
// <body>
//     <div class="card">
//         <h1>Hello from ESP32-S3!</h1>
//         <p>Your local HTML file is successfully hosted.</p>
//     </div>
// </body>
// </html>
// )=====";
//
// // Function that handles the root URL path "/"
// void handleRoot() {
//     server.send(200, "text/html", HTML_CONTENT);
// }
//
// // Function to handle 404 Not Found errors
// void handleNotFound() {
//     server.send(404, "text/plain", "404: Not Found");
// }
//
// void setup() {
//     Serial.begin(115200);
//
//     // Connect to Wi-Fi
//     WiFi.begin(ssid, password);
//     Serial.print("Connecting to Wi-Fi");
//     while (WiFi.status() != WL_CONNECTED) {
//         delay(500);
//         Serial.print(".");
//     }
//
//     // Print local IP Address
//     Serial.println("");
//     Serial.print("Connected! IP address: ");
//     Serial.println(WiFi.localIP());
//
//     // Define URL routing
//     server.on("/", handleRoot);
//     server.onNotFound(handleNotFound);
//
//     // Fire up the server
//     server.begin();
//     Serial.println("HTTP server started");
// }
//
// void loop() {
//     // Listen for incoming client connections
//     server.handleClient();
// }
#include <Arduino.h>
#include <Wire.h>
#include <U8g2lib.h>
#include <Adafruit_MLX90614.h>

// -------------------- I2C Pins --------------------
#define SDA_PIN 14
#define SCL_PIN 12

// -------------------- OLED --------------------
U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2(
    U8G2_R0,
    U8X8_PIN_NONE
);

// -------------------- MLX90614 --------------------
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

void setup() {
    Serial.begin(115200);

    // Initialize I2C
    Wire.begin(SDA_PIN, SCL_PIN);
    Wire.setClock(100000);

    // OLED
    u8g2.begin();

    // MLX90614
    if (!mlx.begin()) {
        Serial.println("MLX90614 NOT FOUND!");

        u8g2.clearBuffer();
        u8g2.setFont(u8g2_font_ncenB08_tr);
        u8g2.drawStr(5, 30, "MLX90614 ERROR!");
        u8g2.sendBuffer();

        while (1);
    }

    Serial.println("MLX90614 Ready!");
}

void loop() {

    static int counter = 0;

    float ambient = mlx.readAmbientTempC();
    float object = mlx.readObjectTempC();

    // Serial Monitor
    Serial.print("Ambient: ");
    Serial.print(ambient);
    Serial.print(" C\tObject: ");
    Serial.print(object);
    Serial.println(" C");

    // OLED
    u8g2.clearBuffer();

    u8g2.setFont(u8g2_font_ncenB08_tr);
    u8g2.drawStr(0, 12, "Fire Robot Monitor");

    char buf[20];

    sprintf(buf, "Amb : %.1f C", ambient);
    u8g2.drawStr(0, 28, buf);

    sprintf(buf, "Obj : %.1f C", object);
    u8g2.drawStr(0, 44, buf);

    sprintf(buf, "Cnt : %d", counter);
    u8g2.drawStr(0, 60, buf);

    u8g2.sendBuffer();

    counter++;
    delay(1000);
}
