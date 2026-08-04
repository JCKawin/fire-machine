#include <WiFi.h>
#include <WebServer.h>

// Replace with your actual network credentials
const char* ssid = "JCKAWIN";
const char* password = "12345678";

// Start the web server on port 80 (HTTP standard)
WebServer server(80);

// Your HTML page, stored inside raw literal string R"=====( ... )====="
const char HTML_CONTENT[] PROGMEM = R"=====(
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 Web Server</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background-color: #f4f4f9; }
        h1 { color: #333; }
        p { color: #666; font-size: 1.2rem; }
        .card { background: white; padding: 20px; display: inline-block; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="card">
        <h1>Hello from ESP32-S3!</h1>
        <p>Your local HTML file is successfully hosted.</p>
    </div>
</body>
</html>
)=====";

// Function that handles the root URL path "/"
void handleRoot() {
    server.send(200, "text/html", HTML_CONTENT);
}

// Function to handle 404 Not Found errors
void handleNotFound() {
    server.send(404, "text/plain", "404: Not Found");
}

void setup() {
    Serial.begin(115200);

    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    // Print local IP Address
    Serial.println("");
    Serial.print("Connected! IP address: ");
    Serial.println(WiFi.localIP());

    // Define URL routing
    server.on("/", handleRoot);
    server.onNotFound(handleNotFound);

    // Fire up the server
    server.begin();
    Serial.println("HTTP server started");
}

void loop() {
    // Listen for incoming client connections
    server.handleClient();
}
