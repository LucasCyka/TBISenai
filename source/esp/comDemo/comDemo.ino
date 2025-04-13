char buffer[4];
unsigned char comandoAtual      = 0;
unsigned char comandoParametro  = 0;

bool comutaLed(){
  digitalWrite(2,!digitalRead(2));

  return true;
}

void setup() {
  pinMode(2,OUTPUT);
  Serial.begin(115200);
}

void loop() {

  if (comandoAtual != 0){ //executa comando
    
    if(comandoAtual == 0x04){ //comando comuta led

      if(comutaLed()){
        comandoAtual      = 0;
        comandoParametro  = 0;
        //sinaliza interface que comando foi executado com sucesso
        Serial.println("END");
      }else{
        //tratamento de erros?
      }
    }
    if(comandoAtual == 0x02){ //teste de curva
      
      for(int i = 0; i < 1000; i++){
        Serial.println((float)i * 1.0,2); //simulacao de valors do sensores enquanto o dc e alterado
        delay(2);
      }


      Serial.println("END");
      comandoAtual     = 0;
      comandoParametro = 0;
    }
    if(comandoAtual == 0x03){ //muda dc maximo
      Serial.println("END");

      comandoAtual     = 0;
      comandoParametro = 0;
    }

    if(comandoAtual == 0x0A){ //Envia dados dos sensores
      Serial.println(3.3); //exemplo de envio
      delay(500);
      Serial.println(0.5);
      delay(500);

      Serial.println("END");

      comandoAtual     = 0;
      comandoParametro = 0;
    }

  }

  if(Serial.available() > 1){
    Serial.readBytes(buffer,4);

    if(buffer[0] == 0x01 && buffer[3] == 0xAA){ //comando = possui 4 bytes, começa com 0x01 e termina com 0xAA
      comandoAtual     = buffer[1];
      comandoParametro = buffer[2];
    }

  }

}


