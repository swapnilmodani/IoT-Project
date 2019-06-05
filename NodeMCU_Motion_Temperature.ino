int outputpin= A0;
int sensor_pin = 16; // Initialized the pin for motion sensor
int relay_pin = 10;
int output = 0;// Variable to store the output state of motion sensor
int preoutput;
void setup(){
  Serial.begin(9600);
  pinMode(sensor_pin, INPUT);   // Declared motion sensor pin as Input
  pinMode(relay_pin, OUTPUT);   // Declared relay module pin as Output pin
  pinMode(5, OUTPUT);   // Declared relay module pin as Output pin
  // Make the relay module initial state as low, Relay works opposite
  digitalWrite(relay_pin, HIGH);
}
void loop(){
  // Read the output state of motion sensor
  preoutput = output;
  output = digitalRead(sensor_pin);

  // If output is High
   if(output == 0 && preoutput == 1){
    delay(7000);
  }
  else if(output == 1){
    digitalWrite(relay_pin, LOW);
    digitalWrite(5, HIGH);
  }
  // If output is LOW
  else if(output == 0){
    digitalWrite(relay_pin, HIGH);
    digitalWrite(5, LOW);
  }
  Serial.println(output);
int analogValue = analogRead(outputpin);
float millivolts = (analogValue/1024.0) * 3300; //3300 is the voltage provided by NodeMCU
float celsius = millivolts/10;
Serial.print("in DegreeC=   ");
Serial.println(celsius);

}
