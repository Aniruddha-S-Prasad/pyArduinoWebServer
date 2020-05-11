#include <Adafruit_Sensor.h>
#include <LiquidCrystal.h>
#include "DHT.h"

// LCD Setup
const int pin_RS = 8; 
const int pin_EN = 9; 
const int pin_d4 = 4; 
const int pin_d5 = 5; 
const int pin_d6 = 6; 
const int pin_d7 = 7; 
const int pin_BL = 10; 
LiquidCrystal lcd( pin_RS,  pin_EN,  pin_d4,  pin_d5,  pin_d6,  pin_d7);

// Problem with LCD backlight, https://forum.arduino.cc/index.php?topic=96747.0
// Use the macros below for the backlight control
#define SafeBLon(pin) pinMode(pin, INPUT)
#define SafeBLoff(pin) pinMode(pin, OUTPUT)


// Global variables

volatile unsigned int msCtr = 0;
volatile byte readFlag = 0;
volatile byte htIdxFlg = 0;
volatile int BL_state = 0;

unsigned int pollTime = 5;
unsigned int pollTime_1 = 2; 
unsigned int pollTimeMs = pollTime*1000;
unsigned int pollTimeMs_1 = pollTime_1*1000;

// DHT Sensor variables
#define DHTTYPE DHT11
#define DHTPIN 3

// Backlight control pn
#define BLCtrlPin 2
DHT dht(DHTPIN, DHTTYPE);
float hmdty, tempCel, htIdx;


void send_dataJson(float temperature, float humidity){
  Serial.print("{\"Temperature\": ");
  Serial.print(temperature);
  Serial.print(",\"Humidity\": ");
  Serial.print(humidity);
  Serial.print("}\n");
}


void setup() {
  // Setup Timer
  // Timer0 i.e. TIMSK0 already initialed by Arduino IDE with prescaler value of 64 to generate a 976.5625 Hz clk
  // Set compare register to 127 = 0x7F
  OCR0A = 0x7F;
  TIMSK0 |= _BV(OCIE0A);
  
  // Setup LCD
  SafeBLon(pin_BL);
  BL_state = 1;
  lcd.begin(16, 2);
  lcd.clear();
  
  // Interrupt to turn BL on or off
  attachInterrupt(digitalPinToInterrupt(BLCtrlPin), BL_CONTROL, RISING);

  Serial.begin(9600);

  // DHT Sensor Setup
  dht.begin();
  delay(3000);
  hmdty = dht.readHumidity();
  tempCel = dht.readTemperature();
}

void loop() {
  if(BL_state >= 1){
    SafeBLon(pin_BL);
  }
  else{
    SafeBLoff(pin_BL);
  }
  if(readFlag == 1){
    readFlag = 0;
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

    //Print function here
    send_dataJson(tempCel, hmdty);
  }
  if(htIdxFlg == 1){
    htIdxFlg = 0;
    htIdx = dht.computeHeatIndex(tempCel, hmdty, false);
    lcd.setCursor(0,1);
    lcd.print("Feels Like: ");
    lcd.print(htIdx);
    lcd.print("C");
  }
}

// Interrupt handler function for the timer interrupt 
// ISR acts like attachInterrupt for internal flags such as TIMER0_COMPA_vect
ISR(TIMER0_COMPA_vect){
  if(msCtr >= pollTimeMs){
    readFlag = 1;
    msCtr = 0;
  }
  else if(msCtr == pollTimeMs_1){
    htIdxFlg = 1;
    msCtr++;
  }
  else{
    msCtr++;
  }
}

void BL_CONTROL() {
  BL_state = !BL_state;
}