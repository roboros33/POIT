float pwm;
float in,out;
float poz_napatie = 1.0;


void setup() {
   pinMode(3, OUTPUT);
   Serial.begin(9600);
}

void loop() {
	
	  in=(float)analogRead(A0)*5/1023;
	  delay(200);
    pwm=poz_napatie/5*255;
    
    analogWrite(3,(int)pwm); 
	  Serial.println(in);
    //Serial.println(poz_napatie);

    
      if (Serial.available() > 0) {
        poz_napatie = Serial.readString().toFloat();
      }                     
  }
