#include <Arduino.h>
#include <ESP32Servo.h>
#include <DHT.h>

// ==========================
// Pin Definitions
// ==========================

// 5-channel flame sensor
#define FLAME_0 19
#define FLAME_1 20
#define FLAME_2 21
#define FLAME_3 47
#define FLAME_4 48

const int flamePins[] = {
    FLAME_0,
    FLAME_1,
    FLAME_2,
    FLAME_3,
    FLAME_4
};

// Servos
#define SERVO0_PIN 3
#define SERVO1_PIN 46

// Buzzer
#define BUZZER_PIN 9

// Motor
#define MOTOR_PIN 11

// MQ-2
#define MQ2_ANALOG 13
#define MQ2_DIGITAL 12

// DHT11
#define DHT_PIN 14
#define DHT_TYPE DHT11


// ==========================
// Objects
// ==========================

Servo servo0;
Servo servo1;

DHT dht(DHT_PIN, DHT_TYPE);


// ==========================
// Setup
// ==========================

void setup()
{
    Serial.begin(115200);
    delay(2000);

    Serial.println();
    Serial.println("=================================");
    Serial.println(" ESP32-S3 SENSOR TEST");
    Serial.println("=================================");

    // --------------------------
    // Flame Sensor
    // --------------------------

    for (int i = 0; i < 5; i++)
    {
        pinMode(flamePins[i], INPUT);
    }

    // --------------------------
    // Buzzer
    // --------------------------

    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);

    // --------------------------
    // Motor
    // --------------------------

    pinMode(MOTOR_PIN, OUTPUT);
    digitalWrite(MOTOR_PIN, LOW);

    // --------------------------
    // MQ2
    // --------------------------

    pinMode(MQ2_ANALOG, INPUT);
    pinMode(MQ2_DIGITAL, INPUT);

    // --------------------------
    // Servos
    // --------------------------

    servo0.setPeriodHertz(50);
    servo1.setPeriodHertz(50);

    servo0.attach(SERVO0_PIN, 500, 2400);
    servo1.attach(SERVO1_PIN, 500, 2400);

    servo0.write(90);
    servo1.write(90);

    // --------------------------
    // DHT11
    // --------------------------

    dht.begin();

    Serial.println("Initialization complete.");
    Serial.println();
}


// ==========================
// Flame Sensor Test
// ==========================

void testFlameSensors()
{
    Serial.println("---- FLAME SENSOR ----");

    for (int i = 0; i < 5; i++)
    {
        int value = digitalRead(flamePins[i]);

        Serial.print("Flame ");
        Serial.print(i);
        Serial.print(" (GPIO ");
        Serial.print(flamePins[i]);
        Serial.print("): ");

        Serial.println(value);
    }
}


// ==========================
// MQ2 Test
// ==========================

void testMQ2()
{
    int analogValue = analogRead(MQ2_ANALOG);
    int digitalValue = digitalRead(MQ2_DIGITAL);

    Serial.println("---- MQ-2 ----");

    Serial.print("Analog GPIO 13: ");
    Serial.println(analogValue);

    Serial.print("Digital GPIO 12: ");
    Serial.println(digitalValue);
}


// ==========================
// DHT11 Test
// ==========================

void testDHT11()
{
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    Serial.println("---- DHT11 ----");

    if (isnan(humidity) || isnan(temperature))
    {
        Serial.println("DHT11 ERROR: Failed to read!");
        return;
    }

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");
}


// ==========================
// Servo Test
// ==========================

void testServos()
{
    Serial.println("---- SERVO TEST ----");

    Serial.println("Moving both servos to 0°");

    servo0.write(0);
    servo1.write(0);
    delay(1000);

    Serial.println("Moving both servos to 90°");

    servo0.write(90);
    servo1.write(90);
    delay(1000);

    Serial.println("Moving both servos to 180°");

    servo0.write(180);
    servo1.write(180);
    delay(1000);

    Serial.println("Returning to 90°");

    servo0.write(90);
    servo1.write(90);
}


// ==========================
// Buzzer Test
// ==========================

void testBuzzer()
{
    Serial.println("---- BUZZER TEST ----");

    // Simple ON/OFF test
    digitalWrite(BUZZER_PIN, HIGH);
    delay(300);

    digitalWrite(BUZZER_PIN, LOW);
    delay(300);

    digitalWrite(BUZZER_PIN, HIGH);
    delay(300);

    digitalWrite(BUZZER_PIN, LOW);
}


// ==========================
// Motor Test
// ==========================

void testMotor()
{
    Serial.println("---- MOTOR TEST ----");

    Serial.println("Motor ON");

    digitalWrite(MOTOR_PIN, HIGH);
    delay(2000);

    Serial.println("Motor OFF");

    digitalWrite(MOTOR_PIN, LOW);
}


// ==========================
// Main Loop
// ==========================

void loop()
{
    Serial.println();
    Serial.println("=================================");
    Serial.println(" SENSOR READINGS");
    Serial.println("=================================");

    // Sensors
    testFlameSensors();
    testMQ2();
    testDHT11();

    Serial.println();

    // Actuators
    testServos();
    testBuzzer();
    testMotor();

    Serial.println();
    Serial.println("Waiting 3 seconds...");
    delay(3000);
}