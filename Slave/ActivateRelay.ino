/*
  Blink adapted 
  Turn the motor on and off.

  Jube Schi
 */

//Activate the relay on digital output 4

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin 4 as an output.
  pinMode(4, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(4, HIGH);   // turn the motor on (HIGH is the voltage level)
  delay(1000);              // wait for n seconds
  digitalWrite(4, LOW);    // turn the motor off by making the voltage LOW
  delay(3000);              // wait for n seconds
}
