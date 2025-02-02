#include <LiquidCrystal.h>

//selection
#define s0  5
#define s1  6
#define s2  7
//tbi pins
#define p0  8
#define p1  9
#define p2  10
#define p3  11
#define p4  12
#define p5  13
//lcd pins
#define d7  17
#define d6  16
#define d5  15
#define d4  4
#define rs  19
#define en  18

unsigned char sel = 0b000;
LiquidCrystal lcd(rs,en,d4,d5,d6,d7);

void setup(){

  lcd.begin(16,2);
  lcd.print("LCD");

  pinMode(s0,OUTPUT);
  pinMode(s1,OUTPUT);
  pinMode(s2,OUTPUT);

  pinMode(A0, INPUT);

  pinMode(p0,OUTPUT);
  pinMode(p1,OUTPUT);
  pinMode(p2,OUTPUT);
  pinMode(p3,OUTPUT);
  pinMode(p4,OUTPUT);
  pinMode(p5,OUTPUT);

  //all tbi pins start high
  digitalWrite(p0,HIGH);
  digitalWrite(p1,HIGH);
  digitalWrite(p2,HIGH);
  digitalWrite(p3,HIGH);
  digitalWrite(p4,HIGH);
  digitalWrite(p5,HIGH);
  
  lcd.clear();

  for(int pin = p0; pin < (p5+1); pin++){
    sel = pin - p0; 

    //select pin to read from demux
    digitalWrite(s0, (sel & 1));
    digitalWrite(s1, (sel & 2));
    digitalWrite(s2, (sel & 4));


    for(int nPin = p0; nPin < (p5 + 1); nPin++){
      if(nPin == pin) {continue;}

      digitalWrite(nPin, LOW);
      int reading = analogRead(A0);

      lcd.print(reading,DEC);
      delay(5000);

      digitalWrite(nPin, HIGH);
      lcd.clear();
    }

    



  }


}


void loop(){

}










