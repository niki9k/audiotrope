#define ledPin 12
#define sensorPin 13


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(sensorPin,INPUT); 
  pinMode(ledPin,OUTPUT);
  
  

}

unsigned long previousTime = 0;
unsigned long timeNow;
unsigned long elapsedTime;
int frame;

void loop() {

  // put your main code here, to run repeatedly:
  while (!digitalRead(sensorPin));
  timeNow = millis();
  elapsedTime = timeNow - previousTime;
  //Serial.println(elapsedTime);
  previousTime = timeNow;
  
  if ((elapsedTime > 20) && (elapsedTime < 100)){
    frame = 16;
    Serial.println(frame);
    delayMicroseconds(1000);
    //Serial.println(elapsedTime);

  }
  else if (elapsedTime > 100){
    if (frame == 16){
      frame = 0;
    }
    else{
      frame++;
    }
    Serial.println(frame);
    //Serial.println(elapsedTime);
    digitalWrite(ledPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(ledPin, LOW);

  }

  while (digitalRead(sensorPin));

}

