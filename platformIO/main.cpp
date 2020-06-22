/*
 * Weather Monitor (DHT11 and ATmega 328P)
 * Author : Aniruddha Prasad
 */ 

#include <Arduino.h>
#include <avr/sleep.h>
#include <LiquidCrystal.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

// DHT Sensor variables
#define DHTTYPE DHT11
#define DHTPIN 3

// LCD Setup
#define D4  4
#define D5  5
#define D6  6
#define D7  7
#define RS  8
#define EN  9
#define BL  10

// Problem with LCD backlight, https://forum.arduino.cc/index.php?topic=96747.0
// Use the macros below for the backlight control
#define SafeBLon(pin) pinMode(pin, INPUT)
#define SafeBLoff(pin) pinMode(pin, OUTPUT)

// Global variables
volatile byte readFlag = false;
volatile byte htIdxFlg = false;
volatile byte BL_state = false;
volatile uint16_t buttonInput = 2000;
float hmdty, tempCel, htIdx;

LiquidCrystal lcd(RS,  EN,  D4,  D5,  D6,  D7);
DHT dht(DHTPIN, DHTTYPE);

void BL_CONTROL(void);
void send_data_json(float temperature, float humidity);


void setup() {
	pinMode(13, OUTPUT);
	digitalWrite(13, LOW);

	// Setup Timer1
	noInterrupts();
	TCCR1A = 0;
	TCCR1B = 0;
	TCNT1 = 3035;						// Timer starts counting from this value, which gives a total of 4s count time in a 16bit timer
										// Formula: TCNT1 = 65535 - (4*16*10^6)/1024 => (Overflow Value) - (seconds*cpu_freq)/prescaler
	OCR1A = 31250;                    	// Two seconds after previous value
	TCCR1B |= (1<<CS10)|(1<<CS12);		// Set prescaler to 1024
	TIMSK1 |= (1<<TOIE1)|(1<<OCIE1A);	// Attach Overflow and Compare Interrupts
	interrupts();

	// Setup LCD
	lcd.begin(16, 2);
	lcd.clear();
	lcd.print("Weather Station");
	SafeBLon(BL);
	BL_state = true;

	// DHT Sensor Setup
	dht.begin();
	delay(1000);

	Serial.begin(9600);
}

void loop() {

	buttonInput = analogRead(A0);
  
	if ((buttonInput > 600) && (buttonInput < 700)){
		BL_CONTROL();
		delay(200);
	}
  
	if(BL_state){
		SafeBLon(BL);
	}
	else{
		SafeBLoff(BL);
	}

	if(readFlag){
		readFlag = false;
		hmdty = dht.readHumidity();
		tempCel = dht.readTemperature();
		lcd.clear();
		lcd.print("Temp: ");
		lcd.print(tempCel);
		lcd.print("C");
		lcd.setCursor(0,1);
		lcd.print("Hmdty: ");
		lcd.print(hmdty);
		lcd.print("%");

		//Print Serial data
		send_data_json(tempCel, hmdty);
	}

	if(htIdxFlg){
		htIdxFlg = false;
		htIdx = dht.computeHeatIndex(tempCel, hmdty, false);
		lcd.setCursor(0,1);
		lcd.print("Feels Like: ");
		lcd.print(htIdx);
		lcd.print("C");
	}

	set_sleep_mode(SLEEP_MODE_IDLE);
	sleep_enable();
	sleep_cpu();
	// sleep_disable();
}

// Interrupt handler function for the timer interrupt 
// ISR acts like attachInterrupt for internal flags such as TIMER1_OVF_vect -> Timer1 Overflow Vector
ISR(TIMER1_OVF_vect){
    TCNT1 = 3035;
	readFlag = true;
}


ISR(TIMER1_COMPA_vect){
	htIdxFlg = true;
}


void BL_CONTROL(void) {
	BL_state = !BL_state;
}


void send_data_json(float temperature, float humidity){
	Serial.print("{\"Temperature\": ");
	Serial.print(temperature);
	Serial.print(",\"Humidity\": ");
	Serial.print(humidity);
	Serial.print("}\n");
}
