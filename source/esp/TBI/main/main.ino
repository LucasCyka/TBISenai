#define INVALID 0
#define CONNECT 1
#define TESTCMD 2

//globals
bool connected = false;

void setup() {
  Serial.begin(115200);

}

void loop() {
    unsigned char msgBuffer[5];

    //deal with messages from the mcu
    if(Serial.available()>0){
      if(Serial.readBytes(msgBuffer,4)){
        
        /**************** connection request *****************/
        if (getMessage(msgBuffer) == CONNECT){ 
          Serial.println("ConnOk"); //just answer
          connected = true;
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
      default:
        decodedMessage = INVALID;
        break;
    }
    

  }else{ //message does not follow specifcation/noise
    return INVALID;
  }

  return decodedMessage;
}





