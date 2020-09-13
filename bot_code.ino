const int trigPin = 9;
const int echoPin = 10;
unsigned long time;
int constant = 1;

int data = 0;

//for strike motor
int strike_pin = 2;

//for buzzer
int buzzer_pin = 3;

//for motor 1 and 2
int in1 = 5;
int in3 = 6;

// defines variables   for ultrasonic sensor
long duration;
int distance;

//for white line sensor
int R_S = A0; //sincer R
int S_S = A1; //sincer S
int L_S = A2; //sincer L
 
void setup() 
{
pinMode(buzzer_pin,OUTPUT);
pinMode(in1, OUTPUT);
pinMode(in3, OUTPUT);
 
pinMode(L_S, INPUT);
pinMode(S_S, INPUT);
pinMode(R_S, INPUT);

pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
pinMode(echoPin, INPUT); // Sets the echoPin as an Input
Serial.begin(9600); // Starts the serial communication

 
}
void loop()
{  

while(Serial.available())
{
  data = Serial.read();
  
}
time = millis();
//Serial.println(data);
if(data == '0')
{
  
  Stop();
}

digitalWrite(trigPin, LOW);
delayMicroseconds(2);
// Sets the trigPin on HIGH state for 10 micro seconds
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
// Reads the echoPin, returns the sound wave travel time in microseconds
duration = pulseIn(echoPin, HIGH);
// Calculating the distance
distance= duration*0.034/2;
//Serial.println(distance);

if(distance<5)
{
  //delay()
  delay(100);
  digitalWrite(in1,LOW);
  digitalWrite(in3,LOW);
  
  
  buzzer_twice();
  strike();  
}
else {
  if ((digitalRead(L_S) == 1)&&(digitalRead(S_S) == 0)&&(digitalRead(R_S) == 1)){forword();}
 
  if ((digitalRead(L_S) == 0)&&(digitalRead(S_S) == 1)&&(digitalRead(R_S) == 1)){turnLeft();}
  if ((digitalRead(L_S) == 0)&&(digitalRead(S_S) ==0)&&(digitalRead(R_S) == 1)) {turnLeft();}
 
  if ((digitalRead(L_S) == 1)&&(digitalRead(S_S) == 0)&&(digitalRead(R_S) == 0)){turnRight();}
  if ((digitalRead(L_S) == 1)&&(digitalRead(S_S) == 1)&&(digitalRead(R_S) == 0)){turnRight();}
 
  if ((digitalRead(L_S) == 1)&&(digitalRead(S_S) == 1)&&(digitalRead(R_S) == 1)){turnLeft();}
}


//void loop ending
}

void strike()
{
  digitalWrite(strike_pin,HIGH);
  delay(1000);
  digitalWrite(strike_pin,LOW); 
  constant = constant +1;
  delay(1000);
  buzzer_once;
}

void buzzer_twice()
{
  digitalWrite(buzzer_pin, HIGH);
  delay(500);
  digitalWrite(buzzer_pin, LOW);
  delay(500);
  digitalWrite(buzzer_pin, HIGH);
  delay(500);
  digitalWrite(buzzer_pin, LOW);
  
}

void buzzer_once()
{
  digitalWrite(buzzer_pin, HIGH);
  delay(500);
  digitalWrite(buzzer_pin, LOW);
  
  
}

void buzzer_five()
{
  digitalWrite(buzzer_pin, HIGH);
  delay(5000);
  digitalWrite(buzzer_pin, LOW);
  delay(50000);
  
}


void forword(){
digitalWrite(in1, HIGH);
digitalWrite(in3,HIGH);
}
 
 
void turnRight(){
digitalWrite(in1, LOW);
digitalWrite(in3, HIGH);
}
 
void turnLeft(){
digitalWrite(in1, HIGH);
digitalWrite(in3, LOW);
}
 
void Stop(){
digitalWrite(in1, LOW);
digitalWrite(in3, LOW);
buzzer_five();
}