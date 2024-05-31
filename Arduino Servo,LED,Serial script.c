#include <Servo.h>

const int servoPin1 = 3;
const int servoPin2 = 5;
const int servoPin3 = 6;

const int LEDpin1 = 9;
const int LEDpin2 = 10;
const int LEDpin3 = 11;

int ledNumber;

Servo servo1;
Servo servo2;
Servo servo3;

int counter1 = 0;
int counter2 = 0;
int counter3 = 0;

struct Hand {
  Servo finger1;
  Servo finger2;
  Servo finger3;
  void reset_fingers(){ //Resets servos
    finger1.write(0);
    finger2.write(0);
    finger3.write(0);
  }
  void reset_leds() { //resets LEDs
    digitalWrite(LEDpin1, LOW);
    digitalWrite(LEDpin2, LOW);
    digitalWrite(LEDpin3, LOW);
  }
  
  int move_fingers(int scenario) { //argument that switches between Case 1 to 6
    switch (scenario) {
      case 1:
        finger1.write(0);
        finger2.write(0);
        finger3.write(0);
        reset_leds();
        digitalWrite(LEDpin1, HIGH);
        Serial.println("Rock");
        break;
      case 2:
        finger1.write(180);
        finger3.write(180);
        finger2.write(180);
        reset_leds();
        digitalWrite(LEDpin2, HIGH);
        Serial.println("Paper");
        break;
      case 3:
        finger1.write(0);
        finger3.write(180);
        finger2.write(180);
        reset_leds();
        digitalWrite(LEDpin3, HIGH);
        Serial.println("Scissors");
        break;
      case 4:
        counter1++;
        delay(5);
        if (counter1 == 1) {
          finger1.write(180);
          digitalWrite(LEDpin1, HIGH);
        } else {
          counter1 = 0;
          finger1.write(0);
          digitalWrite(LEDpin1, LOW);
        }
        Serial.println("moving finger 1");
        break;
      case 5:
        counter2++;
        delay(5);
        if (counter2 == 1) {
          finger3.write(180);
          digitalWrite(LEDpin2, HIGH);
        } else {
          counter2 = 0;
          finger3.write(0);
          digitalWrite(LEDpin2, LOW);
        }
        Serial.println("moving finger 2");
        break;
      case 6:
        counter3++;
        delay(55);
        if (counter3 == 1) {
          finger2.write(180);
          digitalWrite(LEDpin3, HIGH);
        } else {
          counter3 = 0;
          finger2.write(0);
          digitalWrite(LEDpin3, LOW);
        }
        Serial.println("moving finger 3");
        break;
    }
  }
};

Hand hand;

void setup() {
  Serial.begin(115200); //UART init

  hand.finger1.attach(servoPin1);
  hand.finger2.attach(servoPin2);
  hand.finger3.attach(servoPin3);

  pinMode(LEDpin1, OUTPUT);
  pinMode(LEDpin2, OUTPUT);
  pinMode(LEDpin3, OUTPUT);

  // Flush the serial buffer at startup
  while (Serial.available() > 0) {
    Serial.read();
  }

  hand.reset_fingers();
  hand.reset_leds();
//  powerOffAllLEDs();

}

//Acknowladgement message to RPI
void loop() {
  if (Serial.available() > 0) {
    ledNumber = Serial.read() - '0';
    Serial.print("Received: ");
    Serial.println(ledNumber);
    hand.move_fingers(ledNumber);
  }
  

}


