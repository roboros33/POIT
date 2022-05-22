
float in,out;
float poz_napatie = 127;


void setup() {
   pinMode(3, OUTPUT);
   Serial.begin(9600);
}

void loop() {
	
	in=(float)analogRead(A0)*5/1023;
	delay(50);

        analogWrite(3,poz_napatie); 
	Serial.println(in);
	
	if (Serial.read() != -1) {
		poz_napatie = Serial.read();
	}                       
  }
