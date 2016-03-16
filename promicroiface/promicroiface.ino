#include <Keypad.h>
#include "Keyboard.h"

const byte ROWS = 4; // Four rows
const byte COLS = 4; // Three columns

char keys[ROWS][COLS] = {
  {'N','Y','e','A'},
  {'n','y','D','d'},
  {'B','M','T','V'},
  {'b','m','t','v'}
};

// Connect keypad ROW0, ROW1, ROW2 and ROW3 to these Arduino pins.
byte rowPins[ROWS] = { 9, 8, 7, 6 };
// Connect keypad COL0, COL1 and COL2 to these Arduino pins.
byte colPins[COLS] = { 5, 4, 3, 2 }; 

// Create the Keypad
Keypad kpd = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

int ledpin = 17;

void setup()
{
  pinMode(ledpin,OUTPUT);
  digitalWrite(ledpin, HIGH);
  //Serial.begin(9600);
  Keyboard.begin();
  
}

void loop()
{
  char key = kpd.getKey();
  char out;
  if(key)  // Check for a valid key.
  {
    switch (key)
    {
      default:
        Keyboard.print(key);
        //Serial.println(key);
    }
  }
}
