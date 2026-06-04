// ==========================
// EOSAS ARGON HARDWARE CONTROLLER
// Particle Argon - Web IDE Compatible
// ==========================

TCPClient client;

// ==========================
// SERVER SETTINGS
// ==========================

// Default Flask server IP.
// You can update this without reflashing by using Particle Console function:
// Function name: setServerIP
// Argument example: 192.168.1.39
char SERVER_IP[32] = "192.168.1.39";

const int SERVER_PORT = 5000;

// ==========================
// PIN DEFINITIONS
// ==========================

const int BUTTON_PIN = D2;

const int WHITE_LED_LEFT = D3;
const int WHITE_LED_RIGHT = D4;

const int GREEN_LED = D5;
const int YELLOW_LED = D6;
const int RED_LED = D7;

// ==========================
// BUTTON CLICK SETTINGS
// ==========================

unsigned long lastClickTime = 0;
int clickCount = 0;

const unsigned long DOUBLE_CLICK_TIME = 500;

// ==========================
// FUNCTION DECLARATIONS
// ==========================

void startEOSASScan();
void resetSystem();
void allOff();
void allResultLightsOff();
String sendGET(String path);
int setServerIP(String newIP);

// ==========================
// SETUP
// ==========================

void setup() {
    Serial.begin(9600);

    // Allows IP update from Particle Console without reflashing
    Particle.function("setServerIP", setServerIP);

    pinMode(BUTTON_PIN, INPUT_PULLUP);

    pinMode(WHITE_LED_LEFT, OUTPUT);
    pinMode(WHITE_LED_RIGHT, OUTPUT);

    pinMode(GREEN_LED, OUTPUT);
    pinMode(YELLOW_LED, OUTPUT);
    pinMode(RED_LED, OUTPUT);

    allOff();

    Serial.println("=================================");
    Serial.println("EOSAS Argon Hardware Controller");
    Serial.println("Ready");
    Serial.print("Current Flask Server IP: ");
    Serial.println(SERVER_IP);
    Serial.println("=================================");
}

// ==========================
// LOOP
// ==========================

void loop() {

    // Detect button press
    if (digitalRead(BUTTON_PIN) == LOW) {

        clickCount++;
        lastClickTime = millis();

        // Wait until button is released
        while (digitalRead(BUTTON_PIN) == LOW) {
            delay(10);
        }

        // Debounce
        delay(50);
    }

    // Decide single click vs double click
    if (clickCount > 0 && millis() - lastClickTime > DOUBLE_CLICK_TIME) {

        if (clickCount == 1) {
            startEOSASScan();
        }
        else {
            resetSystem();
        }

        clickCount = 0;
    }
}

// ==========================
// MAIN EOSAS SCAN FLOW
// ==========================

void startEOSASScan() {
    Serial.println();
    Serial.println("Single click detected.");
    Serial.println("Starting EOSAS scan...");

    allOff();

    // Turn on scan lighting
    digitalWrite(WHITE_LED_LEFT, HIGH);
    digitalWrite(WHITE_LED_RIGHT, HIGH);

    Serial.println("White LEDs ON.");

    // Tell Flask that a scan is requested
    String startResponse = sendGET("/start_scan");

    Serial.println("Start scan response:");
    Serial.println(startResponse);

    // Keep lighting on while ESP32 captures/uploads
    delay(7000);

    // Turn off scan lighting
    digitalWrite(WHITE_LED_LEFT, LOW);
    digitalWrite(WHITE_LED_RIGHT, LOW);

    Serial.println("White LEDs OFF.");

    // Get latest AI result
    String result = sendGET("/latest_result");

    Serial.println("Latest result response:");
    Serial.println(result);

    allResultLightsOff();

    // Choose LED based on class result
    if (result.indexOf("Low_Hazard") >= 0 ||
        result.indexOf("low_hazard") >= 0 ||
        result.indexOf("Low") >= 0 ||
        result.indexOf("low") >= 0) {

        Serial.println("LED RESULT: GREEN / LOW HAZARD");
        digitalWrite(GREEN_LED, HIGH);
    }
    else if (result.indexOf("Medium_Hazard") >= 0 ||
             result.indexOf("medium_hazard") >= 0 ||
             result.indexOf("Medium") >= 0 ||
             result.indexOf("medium") >= 0) {

        Serial.println("LED RESULT: YELLOW / MEDIUM HAZARD");
        digitalWrite(YELLOW_LED, HIGH);
    }
    else if (result.indexOf("High_Hazard") >= 0 ||
             result.indexOf("high_hazard") >= 0 ||
             result.indexOf("High") >= 0 ||
             result.indexOf("high") >= 0) {

        Serial.println("LED RESULT: RED / HIGH HAZARD");
        digitalWrite(RED_LED, HIGH);
    }
    else {
        Serial.println("LED RESULT: UNKNOWN - DEFAULTING TO YELLOW");
        digitalWrite(YELLOW_LED, HIGH);
    }
}

// ==========================
// RESET SYSTEM
// ==========================

void resetSystem() {
    Serial.println();
    Serial.println("Double click detected.");
    Serial.println("Resetting EOSAS LEDs...");

    allOff();
}

// ==========================
// LED HELPERS
// ==========================

void allOff() {
    digitalWrite(WHITE_LED_LEFT, LOW);
    digitalWrite(WHITE_LED_RIGHT, LOW);

    digitalWrite(GREEN_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, LOW);
}

void allResultLightsOff() {
    digitalWrite(GREEN_LED, LOW);
    digitalWrite(YELLOW_LED, LOW);
    digitalWrite(RED_LED, LOW);
}

// ==========================
// HTTP GET REQUEST HELPER
// ==========================

String sendGET(String path) {
    String response = "";

    Serial.print("Connecting to Flask server at ");
    Serial.print(SERVER_IP);
    Serial.print(":");
    Serial.println(SERVER_PORT);

    if (client.connect(SERVER_IP, SERVER_PORT)) {

        client.println("GET " + path + " HTTP/1.1");
        client.println("Host: " + String(SERVER_IP));
        client.println("Connection: close");
        client.println();

        unsigned long timeout = millis();

        while (client.connected() && millis() - timeout < 5000) {
            while (client.available()) {
                char c = client.read();
                response += c;
            }
        }

        client.stop();
    }
    else {
        Serial.println("Connection to Flask failed.");
    }

    return response;
}

// ==========================
// PARTICLE CLOUD FUNCTION
// UPDATE SERVER IP WITHOUT REFLASHING
// ==========================

int setServerIP(String newIP) {

    if (newIP.length() == 0 || newIP.length() >= sizeof(SERVER_IP)) {
        Serial.println("Invalid IP received.");
        return -1;
    }

    newIP.toCharArray(SERVER_IP, sizeof(SERVER_IP));

    Serial.println();
    Serial.print("New Flask Server IP set to: ");
    Serial.println(SERVER_IP);

    return 1;
}