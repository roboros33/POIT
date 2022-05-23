float temp;
float in,out;
float poz_napatie = 1.0;
static char buffer[32];
static size_t pos = 0;

void setup() {
   	pinMode(3, OUTPUT);
   	Serial.begin(9600);
   	//temp=poz_napatie/5*255;
}

void loop() {
	in=(float)analogRead(A0)*5/1023;
	delay(200);
    	if (poz_napatie != -1 ){
    		temp=poz_napatie/5*255;
    	}
    
    	analogWrite(3,(int)temp); 
	Serial.println(in);
    	//Serial.println(poz_napatie);
	  
	while (Serial.available() > 0) {
      		char c = Serial.read();
        	if (c == '\n') {  
            		float value = atof(buffer);
            		poz_napatie = value;
            		Serial.println(value);
            		pos = 0;
        	} else if (pos < sizeof buffer - 1) {  
            	buffer[pos++] = c;
        	}
	}	
}
