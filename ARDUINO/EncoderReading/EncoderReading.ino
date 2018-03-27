#include<Servo.h>
#include <SoftwareSerial.h>
 
Servo ESC; 
SoftwareSerial mySerial(10, 11); // RX, TX
 
int vel = 1000; 
int escPin = 9;

const byte interruptPin = 2;

volatile unsigned long current_time = 0; 
volatile unsigned long previous_time = 0;
volatile unsigned long half_period = 0;
volatile float velocity = 0; 

void setup() {
  
  ESC.attach(escPin);
  ESC.writeMicroseconds(1000); 
  delay(5000);

  // set the data rate for the SoftwareSerial port
  mySerial.begin(57600);
  
  Serial.begin(57600);
  Serial.setTimeout(10);
  
  pinMode(interruptPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), calculatePeriod, RISING);
  

}

void calculatePeriod()
{
  current_time=micros();
  half_period = current_time-previous_time;

  velocity = 3.1416 * 1000000 / (half_period);

  Serial.println(half_period);
  char *c_data = ( char* ) &velocity;
  for( char c_Index = 0 ; c_Index < sizeof( float ) ; mySerial.write( c_data[ c_Index++ ] ) );
  
  previous_time= current_time;
  
}
void loop() 
{
  if(Serial.available() >= 1)
  {
    vel = Serial.parseInt(); 
    if(vel != 0)
    {
      ESC.writeMicroseconds(vel); 
    }
  }
}



