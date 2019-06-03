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
    int max = 80; // Let consider as Height of the Garbage Bin is = 80 cm.
    float diff, perc;
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);s
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = (duration/2) / 29.1;
    diff = max - distance; // 'diff' variable tells u that, how much the Garbage Bin is Left to fill
    perc = (diff/max)*100; // 'perc' variable tells u that, how much percentage the Garbage Bin is filled.
    if (perc>=90)
    {
    Serial.println("Garbage Bin is FULL."); // When the Garbage Bin is filled more than 90%, then this Error Message will Displayed.
    }
    else
    {
    Serial.print("Garbage Bin is Filled ");
    Serial.print(perc);
    Serial.println(" %."); // These 3 Lines are print, that how much the Garbage Bin is Filled...Ex. "Garbage Bin is Filled 70%.".
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

      SensorVal = analogRead(Input);
      if(SensorVal > 100)
      {
        Serial.println("Smoke Detected . . .");

      }

      else
      {
        Serial.println("All Clear . . .");
      }

    delay(500);
}
