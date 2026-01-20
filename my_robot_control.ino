#include <WiFiNINA.h>

// ===== WiFi =====
const char* ssid = "WiFi-LabIoT";
const char* password = "s1jzsjkw5b";

WiFiServer server(1234);

// ===== L298N =====
#define ENA 10
#define ENB 9
#define IN1 2
#define IN2 3
#define IN3 4
#define IN4 5

#define SPEED_FAST 150
#define SPEED_SLOW 120

int currentCmd = 0;

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  Serial.print("Connexion WiFi...");
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connecté !");
  Serial.println(WiFi.localIP());

  server.begin();
  stopMotors();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    while (client.connected()) {
      if (client.available()) {
        String s = client.readStringUntil('\n');
        int cmd = s.toInt();
        currentCmd = cmd;
        handleCommand(currentCmd);
      }
    }
  }
}

// ===== COMMANDES =====
void handleCommand(int v) {
  switch (v) {
    case 0: stopMotors(); break;
    case 1: forward(); break;
    case 2: backward(); break;
    case 3: left(); break;
    case 4: right(); break;
    case 5: forwardLeft(); break;
    case 6: forwardRight(); break;
    case 7: backLeft(); break;
    case 8: backRight(); break;
    default: stopMotors();
  }
}

// ===== MOTEURS =====
void stopMotors() {
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}

// AVANCER
void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);

  digitalWrite(IN3, LOW);  
  digitalWrite(IN4, HIGH);  

  analogWrite(ENA, SPEED_FAST);
  analogWrite(ENB, SPEED_FAST);
}

// RECULER
void backward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);

  digitalWrite(IN3, HIGH);  
  digitalWrite(IN4, LOW);  

  analogWrite(ENA, SPEED_FAST);
  analogWrite(ENB, SPEED_FAST);
}

// GAUCHE (pivoter sur place)
void left() {
  digitalWrite(IN1, LOW);   // gauche recule
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);  // droite avance
  digitalWrite(IN4, LOW);

  analogWrite(ENA, SPEED_FAST);
  analogWrite(ENB, SPEED_FAST);
}

// DROITE (pivoter sur place)
void right() {
  digitalWrite(IN1, HIGH);  // gauche avance
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);   // droite recule
  digitalWrite(IN4, HIGH);

  analogWrite(ENA, SPEED_FAST);
  analogWrite(ENB, SPEED_FAST);
}

// AVANT GAUCHE
void forwardLeft() {
  forward();
  analogWrite(ENA, SPEED_SLOW); // moteur gauche plus lent
}

// AVANT DROITE
void forwardRight() {
  forward();
  analogWrite(ENB, SPEED_SLOW); // moteur droit plus lent
}

// ARRIERE GAUCHE
void backLeft() {
  backward();
  analogWrite(ENA, SPEED_SLOW); // moteur gauche plus lent
}

// ARRIERE DROITE
void backRight() {
  backward();
  analogWrite(ENB, SPEED_SLOW); // moteur droit plus lent
}
