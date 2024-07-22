#include "HX711.h"

#define MAX_BITS 100                 // max number of bits 
#define WEIGAND_WAIT_TIME  3000      // time to wait for another weigand pulse.
#define data 6                       // HX711 data pin
#define clk 7                        // HX711 clock pin

HX711 scale;


unsigned char databits[MAX_BITS];    // stores all of the data bits
unsigned char bitCount;              // number of bits currently captured
unsigned char flagDone;              // goes low when data is currently being captured
unsigned int weigand_counter;        // countdown until we assume there are no more bits
 
unsigned long facilityCode=0;        // decoded facility code
unsigned long cardCode=0;            // decoded card code

// interrupt that happens when INTO goes low (0 bit)
void ISR_INT0() {
  //Serial.print("0");   // uncomment this line to display raw binary
  bitCount++;
  flagDone = 0;
  weigand_counter = WEIGAND_WAIT_TIME;  
 
}
 
// interrupt that happens when INT1 goes low (1 bit)
void ISR_INT1() {
  //Serial.print("1");   // uncomment this line to display raw binary
  databits[bitCount] = 1;
  bitCount++;
  flagDone = 0;
  weigand_counter = WEIGAND_WAIT_TIME;  
}

void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT);     // DATA0 (INT0)
  pinMode(3, INPUT);     // DATA1 (INT1)
 
  Serial.begin(9600);

  attachInterrupt(0, ISR_INT0, FALLING);  
  attachInterrupt(1, ISR_INT1, FALLING);
 
 
  weigand_counter = WEIGAND_WAIT_TIME;

  scale.begin(data, clk);

  scale.set_scale();
  scale.tare();
  //Serial.println("Place 210g now.");
  delay(3000);
  //Serial.println(scale.get_units(10));
  scale.set_scale(436.f);
}

void loop() {
  // put your main code here, to run repeatedly:

  int pthn;
  
  if (Serial.available() > 0){
    pthn = (int) Serial.read();
    pthn -= 48;

    if (pthn == 9){
      //Serial.println((analogRead(loadPin)-125)*0.003);
      scale.power_up();
      Serial.println(scale.get_units());
      scale.power_down();
    }
    else{
      return;
    }
  }
  
  // This waits to make sure that there have been no more data pulses before processing data
  if (!flagDone) {
    if (--weigand_counter == 0)
      flagDone = 1;  
  }
    
  // if we have bits and we the weigand counter went out
  if (bitCount > 0 && flagDone) {
    
    delay(100);
    
    unsigned char i;
    
    for(i=1; i<bitCount-1; i++){
      cardCode <<= 1;
      cardCode |= databits[i];
    }
    Serial.print(cardCode);
    delay(2000);
    Serial.print("\n");
    //Serial.println((analogRead(loadPin)-125)*0.003);
    scale.power_up();
    Serial.println(scale.get_units());
    scale.power_down();
    
    // cleanup and get ready for the next card
    bitCount = 0;
    facilityCode = 0;
    cardCode = 0;
    for (i=0; i<MAX_BITS; i++) {
      databits[i] = 0;
    }
  }
}
