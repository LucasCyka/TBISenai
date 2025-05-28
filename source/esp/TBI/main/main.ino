#include "ADS1X15.h"
#include <Wire.h>

//messsages id
#define INVALID   128
#define CONNECT   129
#define TESTCMD   130
#define GETSENSOR 131
#define CONTEST   132

//pins
#define MOTOR_PIN       2
#define OVERCURRENT_PIN 4
#define OVERVOLTAGE_PIN 5
#define CONNLED_PIN     23

//general conf.
#define I2C_SPEED      400000
#define PWM_INTERVAL   50
#define PWM_INCREMENT  1
#define PWM_DECREMENT  1
#define OPEN_INTERVAL  1000

//globals
bool connected         = false;
bool adcConnected      = false;
bool oncurveTest       = false;
bool finisingTest      = false;
bool opening           = true;
int  pwmInterval       = 0;
int  maxDc             = 85; 
int  intervalConnCheck = 0;

ADS1115 ADS(0x48);

void setup() {
  //pins config
  pinMode(MOTOR_PIN,OUTPUT);
  pinMode(OVERCURRENT_PIN,INPUT);
  pinMode(OVERVOLTAGE_PIN,INPUT);
  pinMode(CONNLED_PIN,OUTPUT);

  //ensures the motor will be off
  digitalWrite(MOTOR_PIN,LOW);

  digitalWrite(CONNLED_PIN,LOW);

  //pwm configuration
  ledcAttach(MOTOR_PIN,500,8);

  Serial.begin(230400);
  Serial.setTimeout(1000); 
  //Wire.begin(14,27); //TODO: remove on final product
  adcSetup(); 
}

void loop() {


    unsigned char msgBuffer[5];
    if(oncurveTest) {curveTest();}
    else{
      if ((millis() - intervalConnCheck) >= 3000 &&  Serial.available() == 0){
        digitalWrite(CONNLED_PIN,LOW);
      }
    }
    //TODO: if there was a connection, check if its on
    
    //deal with messages from the mcu
    if(Serial.available()>0){
      if(Serial.readBytes(msgBuffer,4)){
        
        /**************** connection request *****************/
        if (getMessage(msgBuffer) == CONNECT){ 
          Serial.println("ConnOk"); //just answer
          connected = true;
          intervalConnCheck = millis();
          digitalWrite(CONNLED_PIN,HIGH);
        }


        /**************** pin 2 comutation *****************/
        if (getMessage(msgBuffer) == TESTCMD){ 
          //TODO: ignore this, it can fry the motor
          //digitalWrite(MOTOR_PIN,!digitalRead(MOTOR_PIN));
          Serial.println("END"); 
        }

        /**************** curve test *****************/
        if (getMessage(msgBuffer) == TESTCMD){ 
          Serial.println("END"); //tell the interface the command has been understood and will be executed
          oncurveTest = true;
          opening     = true;
        }

        /**************** get sensor data *****************/
        if (getMessage(msgBuffer) == GETSENSOR){ 
          Serial.println("END"); //tell the interface the command has been understood and will be executed
          int tps1 = ADS.readADC(0); 
          int tps2 = ADS.readADC(1);  

          Serial.println(ADS.toVoltage(tps1),3);
          delay(1);
          Serial.println(ADS.toVoltage(tps2),3);
        }

      }

    }
}

//decode a message from the interface
int getMessage(unsigned char *msg){
  int decodedMessage;

  if (msg[0] == 0x01 && msg[3] == 0xAA){
    
    switch(msg[1]){
      case 0x05: 
        decodedMessage = CONNECT;
        break;
      case 0x04:
        decodedMessage = TESTCMD;
        break;
      case 0x0A:
        decodedMessage = GETSENSOR;
        break;
      default:
        decodedMessage = INVALID;
        break;
    }
    

  }else{ //message does not follow specifcation/noise
    return INVALID;
  }

  return decodedMessage;
}

void adcSetup(){
  Wire.begin(21,22); TODO: add again on final product
  if (ADS.begin()){

    ADS.setDataRate(7);
    ADS.setGain(1);
    ADS.setWireClock(400000);

    if(ADS.isConnected()){
      adcConnected = true;
    }
  }

}

void curveTest(){
  int tps1 = ADS.readADC(0); 
  int tps2 = ADS.readADC(1);  

  Serial.println(ADS.toVoltage(tps1),3);
  delay(1); //due to uart speed, can decrease it with higher baud
  Serial.println(ADS.toVoltage(tps2),3);

  if (finisingTest){

    if ((millis() - pwmInterval) > 3000){
      ledcWrite(MOTOR_PIN,0);
      oncurveTest  = false;
      finisingTest = false;
      opening     = true;
      Serial.println("END");
    }

    return;
  }

  if((millis() - pwmInterval) > PWM_INTERVAL){
    pwmInterval = millis();
    int currentDC = ledcRead(MOTOR_PIN);

    if(opening){

      if (currentDC >= maxDc){opening = false;}

      ledcWrite(MOTOR_PIN,currentDC + PWM_INCREMENT);

    }else{

      if(currentDC > 0){
        ledcWrite(MOTOR_PIN,currentDC - PWM_DECREMENT);
      }else{
        finisingTest = true;
      }

      

    }

  }

}

void checkIssues(){

  if(digitalRead(OVERCURRENT_PIN)){
    oncurveTest = false;
    ledcWrite(MOTOR_PIN,0);

    //TODO: raise exception to the interface
  }

    if(digitalRead(OVERVOLTAGE_PIN)){
    oncurveTest = false;
    ledcWrite(MOTOR_PIN,0);

    //TODO: raise exception to the interface
  }

}

