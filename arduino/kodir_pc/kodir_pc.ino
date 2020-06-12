#include <IRremote.h>

/*****************************************************************************
 *                              Configurações
 *****************************************************************************/
#define IR_PIN      10       // Pino do leitor IR
#define IR_CMD_PRE  "IR_"    // Prefixo que será adicionado ao enviar um comando IR pelo serial
#define IR_DELAY    100      // Delay entre as leituras (tempo em ms)

#define CTL_ON_1  "6D8867D7" // Código 1 do botão de power
#define CTL_ON_2  "2FD48B7"  // Código 2 do botão de power
#define CTL_ON_3  "692D04A0" // Código 3 do botão de power
#define CTL_ON_PIN_IN   2    // Pino para verificar o estado do computador (POWER LED +)
#define CTL_ON_PIN_OUT  3    // Pino para ligar o computador (POWER SW +)
#define CTL_PULSE_TIME  500  // Tempo em ms do pulso de power

#define END_BYTE  "\n"       // Carac. final ao enviar uma mensagem pelo serial ("\n" é o mesmo que (char) 0x0A)

/*****************************************************************************
 *                              Variáveis
 *****************************************************************************/
// IR
IRrecv irrecv(IR_PIN);
decode_results results;
unsigned long irTimeNow = 0;
unsigned long irMillis  = 0; 

// Controller
String serialCmd = "";
String irCmd = "";
int i = 0;

void setup(){
    // Configurações de IO
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(CTL_ON_PIN_OUT, OUTPUT);
    pinMode(CTL_ON_PIN_IN, INPUT);

    digitalWrite(LED_BUILTIN, LOW);
    digitalWrite(CTL_ON_PIN_OUT, LOW);

    // Configurações de bibliotecas
    irrecv.enableIRIn();

    // Configurações do algoritmo
    Serial.begin(9600);
}
 
void loop(){
    serialHandle();
    irHandle();
}

/*****************************************************************************
 *                                    Serial
 *****************************************************************************/
void serialReceive(){
    if (Serial.available() > 0){
        serialCmd = Serial.readString();
        serialCmd.replace(END_BYTE, "");
    }
}

void serialSend(String value, boolean endLine){
    if (Serial.availableForWrite() > 0){
        Serial.print(value);

        if (endLine)
            Serial.print(END_BYTE);
    }
}

void serialHandle(){
    // Receber os dados via serial
    serialReceive(); 

    // Há algum comando a ser executado?
    if (serialCmd.length() > 0){
        // Responder ao ping
        if (serialCmd.equalsIgnoreCase(F("PING")))
            serialSend(F("PONG"), true);
        
        serialCmd = ""; // Limpar o comando
    }
}

/*****************************************************************************
 *                                     IR
 *****************************************************************************/
void irRead(){
    irMillis = millis();

    if (irMillis < irTimeNow) 
        irTimeNow = irMillis;

    else if (irMillis - irTimeNow > IR_DELAY && irCmd.length() <= 0) {
        irTimeNow = irMillis;

        if (irrecv.decode(&results)) {
            irCmd = String(results.value, HEX);
            irCmd.toUpperCase();
            irrecv.resume();

            digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
        }
    }
}

void irHandle(){
    // Executar leitura
    irRead();

    // Responder ao comando IR
    if (irCmd.length() > 0){

        // Aciona o botão de power do computador somente se estiver desligado
        if (irCmd.equals(F(CTL_ON_1)) || irCmd.equals(F(CTL_ON_2)) || irCmd.equals(F(CTL_ON_3))){
            if (digitalRead(CTL_ON_PIN_IN) == LOW){
                // Ligar o PC (press. pw)
                digitalWrite(CTL_ON_PIN_OUT, HIGH);
                delay(CTL_PULSE_TIME);
                digitalWrite(CTL_ON_PIN_OUT, LOW);
            }
        }

        serialSend(IR_CMD_PRE, false);
        serialSend(irCmd, true);

        irCmd = "";
    }
}
