# Arduino
DEVICE_VID = "" # "1A86"
DEVICE_PID = "" # "7523"

# Comunicacao
CON_BAUD_RATE           = 9600    # Velocidade da comunicacao
CON_END_BYTE            = b'\n'   # Carac. para de fim da mens.
CON_ENCODE_DECODE       = "utf-8" # Encode
CON_PING_TIMEOUT        = 5       # Tempo para cada tent. (em segundos) (0 = no timeout; -1 = forever timeout)
CON_PING_ATTEMPT        = 3       # Tentativas para o ping-pong
CON_RECEIVE_TIMEOUT     = 1       # Tempo para receber uma mens. (em segundos) (0 = no timeout; -1 = forever timeout)
CON_SERIAL_READ_TIMEOUT = 1       # Tempo de leitura do serial (em segundos)

# Controle
CTL_IR_PRE          = "IR_" # Flag para verificar se o comando e do leitor
CTL_KEY_DELAY       = 0.25  # Delay entre o press. das teclas (em segundos)
CTL_KEY_CONFIG_TIME = 50    # x200ms
CTL_WINDOW_PROPERTY = 10000 # Variaveis

# Settings
SET_WINDOW_ID = 10140 # Settings window
#SET_WINDOW_NUM_ID = 10109
