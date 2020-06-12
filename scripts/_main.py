import _kodi as Kodi
kodi = Kodi.Kodi()

import datetime, time, serial, serial.tools.list_ports

# Classe responsavel pela comunicacao com o Arduino
class Connection():
    
    class device: None

    def __init__(self, vid, pid):
        self.device.vid = vid
        self.device.pid = pid
        self.device.id = vid + ":" + pid
        self.device.port = None
        self.device.desc = None
        self.serial = None

    # Scanea os dispositivos disponiveis
    def scan(self):
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
            if self.device.id in hwid:
                self.device.port = port
                self.device.desc = desc
                return
        
        # Nao encontrou o dispositivo
        self.device.port = None
        self.device.desc = None
    
    # Inicia a comunicacao com o dispositivo
    def begin(self):
        try:
            if self.device.port == None:
                raise

            self.serial = serial.Serial(
                self.device.port, kodi.config.CON_BAUD_RATE, serial.EIGHTBITS, 
                serial.PARITY_NONE, serial.STOPBITS_ONE, kodi.config.CON_SERIAL_READ_TIMEOUT
            )

            kodi.showPopup("{} '{}' {} {} bit/s".format(kodi.getLocalizedString(32073), self.device.port, kodi.getLocalizedString(32074), kodi.config.CON_BAUD_RATE))
            return True
        except:
            kodi.showPopup(kodi.getLocalizedString(32072), "ERROR")
            self.serial = None
            return False

    # Parar a comunicacao
    def stop(self):
        if self.serial:
            self.serial.cancel_read()
            self.serial.cancel_write()
            self.serial.close()
            self.device.port = None
            self.device.desc = None

    # Loop ate receber uma mensagem completa
    def receive(self, timeout = kodi.config.CON_RECEIVE_TIMEOUT):
        try:
            if self.serial == None:
                kodi.showPopup (kodi.getLocalizedString(32071), "ERROR")
                raise

            time_init = datetime.datetime.now()
            date_timeout = datetime.timedelta(seconds=timeout)            
            message = ""

            while True:
                byte = self.serial.read()
                
                if byte == kodi.config.CON_END_BYTE:
                    return message
                else:
                    message = message + byte.decode(kodi.config.CON_ENCODE_DECODE)

                if timeout > -1 and (datetime.datetime.now() - time_init) > date_timeout:
                    raise

                kodi.loopMonitor(self.serial)
                
        # Erro para o timeout        
        except Exception:
            return None

    # Envia uma mensagem ao arduino
    def send(self, msg):
        self.serial.write(msg.encode(kodi.config.CON_ENCODE_DECODE))
        self.serial.write(kodi.config.CON_END_BYTE)

    # Executar o comando de ping
    def ping(self):
        attempt = kodi.config.CON_PING_ATTEMPT

        while attempt:   
            kodi.loopMonitor(self.serial)
                   
            attempt = attempt - 1
            
            self.send("PING")
            
            if self.receive(kodi.config.CON_PING_TIMEOUT) != None:
                kodi.setConnected(self.device)
                return True
            
        kodi.setDisconnected()
        kodi.showPopup(kodi.getLocalizedString(32070), "ERROR")
        return False
    
# Classe responsavel pelo controle do sistema
class Controller():
    time_last_key = datetime.datetime.now() 

    def __init__(self):
        self.conn = Connection(kodi.config.DEVICE_VID, kodi.config.DEVICE_PID)

    # Executa em loop de 500ms ate conectar-se com sucesso e executar um ping-pong
    def connect(self):

        print_header = True

        while True:
            kodi.loopMonitor(self.conn.serial)

            try:
                # Envita que os comando sejam executados rapidamente
                if print_header:
                    kodi.showPopup(kodi.getLocalizedString(32069))

                #self.conn.setDevice(kodi.config.DEVICE_VID, kodi.config.DEVICE_PID)
                self.conn.scan()

                if self.conn.device.port == None:
                    print_header = False
                
                else:
                    kodi.showPopup("{} '{}'".format(kodi.getLocalizedString(32068), self.conn.device.port))
                    
                    kodi.showPopup(kodi.getLocalizedString(32067))
                    if self.conn.begin():
                        kodi.showPopup(kodi.getLocalizedString(32066), None, None, 1000)

                        if self.conn.ping():
                            #kodi.mapper.setSettingsFields()
                            kodi.showPopup(kodi.getLocalizedString(32065))
                            return
                        else:
                            print_header = True
                    else:
                        kodi.showPopup(kodi.getLocalizedString(32064), "ERROR")
                        print_header = True
            except:
                kodi.showPopup(kodi.getLocalizedString(32063), "ERROR")
                print_header = True
                time.sleep(5)

            kodi.loopMonitor(self.conn.serial)
            time.sleep(1)

    # Executa um comando
    def irHandler(self, hex):
        kodi.handlerKeyPressed(hex)

        if kodi.mapper.containsValue(hex):
            # Envita que os comando sejam executados rapidamente
            if datetime.datetime.now() - self.time_last_key > datetime.timedelta(seconds=kodi.config.CTL_KEY_DELAY):
                self.time_last_key = datetime.datetime.now()
            else:
                return

            try:
                kodi.execAction(kodi.mapper.getKeyByValue(hex).getAction())
            except:
                kodi.showPopup("{} '{}'".format(kodi.getLocalizedString(32062), hex), "ERROR")

    # Executa em loop respondendo aos comandos
    def run(self, loop = True): 
  
        self.connect() # Conectar ao arduino
        command = None

        while loop:
            kodi.loopMonitor(self.conn.serial)

            command = self.conn.receive(-1) # Fica parado aqui ate receber uma mensagem do arduino

            if command != None: # Algum comando valido foi recebido?
                if command.startswith(kodi.config.CTL_IR_PRE): # Comando contem a flag do IR?
                    command = command.replace(kodi.config.CTL_IR_PRE, "")
                    self.irHandler(command)
            else:
                kodi.setDisconnected()
                kodi.showPopup(kodi.getLocalizedString(32061), "ERROR")
                self.connect() # reconectar ao Arduino

        return command

