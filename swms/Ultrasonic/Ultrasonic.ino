#define trigPin 12
#define echoPin 13
int Input = A0;
int SensorVal = 0;

int Check = 0;

void setup()
{
Serial.begin (9600);
pinMode(trigPin, OUTPUT);
pinMode(echoPin, INPUT);
  pinMode(Input, INPUT);
}
void loop()
{
long duration, distance;
float diff, perc;
digitalWrite(trigPin, LOW);
delayMicroseconds(2);
digitalWrite(trigPin, HIGH);
delayMicroseconds(10);
digitalWrite(trigPin, LOW);
duration = pulseIn(echoPin, HIGH);
distance = (duration/2) / 29.1;
diff= 26.25 - distance;
perc = (diff/26.25)*100; // 'perc' variable tells u that, how much percentage the Garbage Bin is filled.

if (perc >= 80)
{
Serial.print("100"); // When the Garbage Bin is filled more than 90%, then this Error Message will Displayed.
}
else if(perc <= 1) {
  Serial.print("0");
}
else
{

Serial.print(perc);

}

/*
if (distance >= 400 || distance <= 2)
{
Serial.println("Out of range");
}
else
{
Serial.print(distance);
Serial.println(" cm");
}
*/
Serial.print(",");

  SensorVal = analogRead(Input);
  if(SensorVal > 100) 
  {
    Serial.println("1");
   
  }

  else
  {
    Serial.println("0");
  }
  
delay(2000);
}
