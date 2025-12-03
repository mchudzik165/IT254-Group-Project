
#include <Servo.h>

Servo myservo;
int servoPin = 9;

void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin);
  myservo.write(0); // Door closed
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    if (c == 'O') {          // Open command from Python
      myservo.write(90);     // Rotate to open the door
      delay(500);
    }

    if (c == 'C') {          // Close command from Python
      myservo.write(0);
      delay(500);
    }
  }
}
