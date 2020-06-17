import xbmc, xbmcaddon, xbmcvfs, xbmcgui, os
import time, json, datetime
import struct

class Kodi():

    def __init__(self):
        self.monitor = None
        self.addon = xbmcaddon.Addon()

        # Carregar user path
        self.user_data = xbmc.translatePath(self.addon.getAddonInfo('profile')).decode('utf-8')
        self.settings_json = os.path.join(self.user_data, 'settings.json')
        self.resources = os.path.join(self.addon.getAddonInfo("path").decode('utf-8'), "resources")

        import _mapper
        self.mapper = _mapper

        import _config
        self.config = _config

    #############################################################
    #                          Monitor
    #############################################################
    # Ativar o monitor de eventos do kodi
    def enableMonitor(self):
        self.monitor = xbmc.Monitor()
        self.reload_fields = True

    # Executa o monitor de eventos
    def loopMonitor(self, serial):
        
        if self.monitor:            
            # Quando fechar o kodi 
            if self.monitor.abortRequested():
                if serial:
                    serial.close()              
                
                self.saveSettings()

                import sys
                sys.exit(0)

            # Quando abrir a janela de config.
            else:
                # Se janela aberta
                if self.isSettingsOpen():
                    # Se recarregar os campos
                    if self.reload_fields:
                        # Atualizar campos
                        self.mapper.setSettingsFields(self.addon)
                        self.reload_fields = False

                    # Tratar a insercao de valores
                    self.handlerInput()

                # Recarregar campos quando abri-la
                elif not self.reload_fields:
                    self.reload_fields = True
            
    #############################################################
    #                          Settings
    #############################################################
    # Verifica se a janela de config. esta aberta
    def isSettingsOpen(self):
        return (xbmcgui.getCurrentWindowDialogId() == self.config.SET_WINDOW_ID)

    # Carrega as config. para a memoria
    def loadSettings(self, saveIfEmpty = True):
        if xbmcvfs.exists(self.settings_json):
            with open(self.settings_json) as infile:
                self.mapper.list_keys = json.load(infile, object_hook = self.mapper.json_decoder)

        # Criar um arquivo
        elif saveIfEmpty:
            self.saveSettings()
    
    # Salva as cong. no disco
    def saveSettings(self):
        if not xbmcvfs.exists(self.user_data):
            xbmcvfs.mkdir(self.user_data)

        #self.mapper.getKeyById("lef").__dict__
        with open(self.settings_json, 'w') as outfile:
            json.dump([ob.__dict__ for ob in self.mapper.list_keys], outfile)

    # Atualiza as contantes (que sao variaveis haha)
    def loadSettingsConsts(self):
        self.config.DEVICE_PID = self.mapper.getKeyById("pid").getValue().upper()
        self.config.DEVICE_VID = self.mapper.getKeyById("vid").getValue().upper()

        self.config.CON_BAUD_RATE       = int(self.mapper.getKeyById("bra").getValue())
        self.config.CON_END_BYTE        = struct.pack("B", int(self.mapper.getKeyById("bfi").getValue()))
        self.config.CON_ENCODE_DECODE   = self.mapper.getKeyById("ede").getValue()
        self.config.CON_PING_TIMEOUT    = int(self.mapper.getKeyById("tmp").getValue()) * .1 # x100ms
        self.config.CON_PING_ATTEMPT    = int(self.mapper.getKeyById("tpg").getValue())
        self.config.CON_RECEIVE_TIMEOUT = int(self.mapper.getKeyById("tmr").getValue()) * .1 # x100ms
        self.config.CON_SERIAL_READ_TIMEOUT = int(self.mapper.getKeyById("tml").getValue()) * .1 # x100ms

        self.config.CTL_IR_PRE = self.mapper.getKeyById("fcm").getValue()
        self.config.CTL_KEY_DELAY = int(self.mapper.getKeyById("dtc").getValue()) * .01 # x10ms
        self.config.CTL_KEY_CONFIG_TIME = int(self.mapper.getKeyById("tjt").getValue())

        self.config.CTL_WINDOW_PROPERTY = int(self.mapper.getKeyById("jva").getValue())
        self.config.SET_WINDOW_ID = int(self.mapper.getKeyById("jcf").getValue())

    # Requisicao para selecionar uma tecla
    def addonSelectKey(self, item_id):
        # Arduino conectado
        if self.getProperty("state_ppt") == self.getLocalizedString(32082):
            self.showPopup(self.getLocalizedString(32075), "ERROR")
            return
        
        key_time = self.config.CTL_KEY_CONFIG_TIME
        dProgress = 0

        # Criar um janela de progresso
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(self.addon.getAddonInfo("name"), self.getLocalizedString(32079))

        self.setProperty("request_select_ppt", item_id)
        last_key = self.getProperty("last_key_ppt")

        time.sleep(0.2)
        
        # Limpa a variavel global e espera ela ser setada 
        while key_time:
            time.sleep(0.2)
            pDialog.update(dProgress, self.getLocalizedString(32079))

            key_time = key_time - 1
            dProgress = dProgress + (100 / self.config.CTL_KEY_CONFIG_TIME)

            # Finalizar o processo
            if pDialog.iscanceled() or not self.getProperty("request_select_ppt"):
                break
        
        # Nenhuma tecla foi press.
        else:
            if self.getProperty("request_select_ppt"):
                self.setProperty("last_key_ppt", last_key)

            # Erro ao receber um valor
            else:            
                self.showPopup(self.getLocalizedString(32076), "ERROR")

        # Zerar a requisicao
        self.setProperty("request_select_ppt", "")

    # Handler para ser executado quando a solicitacao de key estiver ativa
    def handlerKeyPressed(self, command):
        # Se foi solicitado atualizar a propriedade
        if self.getProperty("request_select_ppt"):
            # Tecla ja mapeada
            if self.mapper.isBlacklistUpdate(command):
                # Mesma tecla press.
                if self.getProperty("last_key_ppt") == command:
                    return
                else:
                    self.showPopup(self.getLocalizedString(32077), "ERROR")

            # Evita limpar acoes criticas (a.k.a. select)
            else:
                item_id = self.getProperty("request_select_ppt")

                self.mapper.setUniqueValue(item_id, command)
                self.mapper.setSettingsFields(self.addon)
                self.saveSettings()

            # Informar fim da requisicao
            self.setProperty("request_select_ppt", "")

        # Salvar ultima tecla
        self.setProperty("last_key_ppt", command)

    # Handler para quando solicitar um entrada de dados
    def handlerInput(self):
        request = self.getProperty("request_input")
        
        if request:
            if not self.getProperty("response_input"):
                try:
                    inputDialog = InputDialog(self, request)
                    inputDialog.start()
                    self.setProperty("response_input", "False")
                except:
                    self.setProperty("response_input", "")
                    raise

    #############################################################
    #                          Util
    #############################################################
    # Executa uma acao
    def execAction(self, action):
        if action.startswith("system_b_"):
            action = action.replace("system_b_", "")
            xbmc.executebuiltin(action)
            
        else:
            xbmc.executebuiltin('XBMC.Action(%s)'%(action))

    def setProperty(self, property, value):
        xbmcgui.Window(self.config.CTL_WINDOW_PROPERTY).setProperty(property, value)

    def getProperty(self, _property):
        return str(xbmcgui.Window(self.config.CTL_WINDOW_PROPERTY).getProperty(_property))

    def setConnected(self, device):
        self.mapper.getKeyById("state").setValue(self.getLocalizedString(32081))
        self.mapper.getKeyById("port").setValue(device.port)
        self.mapper.getKeyById("id").setValue(device.id)
        self.mapper.getKeyById("desc").setValue(device.desc)

        self.addon.setSetting("state", self.getLocalizedString(32081))
        self.addon.setSetting("port", device.port)
        self.addon.setSetting("id", device.id)
        self.addon.setSetting("desc", device.desc)

    def setDisconnected(self):
        self.mapper.getKeyById("state").setValue(self.getLocalizedString(32082))
        self.mapper.getKeyById("port").setValue("")
        self.mapper.getKeyById("id").setValue("")
        self.mapper.getKeyById("desc").setValue("")

        self.addon.setSetting("state", self.getLocalizedString(32082))
        self.addon.setSetting("port", "")
        self.addon.setSetting("id", "")
        self.addon.setSetting("desc", "")

    # Exibe uma notificacao na tela
    def showPopup(self, text, i_type = None, title = None, time = 2000):
        if not title:
            title = self.addon.getAddonInfo("name")

        if i_type:
            i_type = os.path.join(self.resources, "error.png")
        else:
            i_type = os.path.join(self.resources, "info.png")

        if i_type:
            xbmc.executebuiltin('Notification({}, {}, {}, {})'.format(title, text, time, i_type))
        else:
            xbmc.executebuiltin('Notification({}, {}, {})'.format(title, text, time))

    def getLocalizedString(self, code):
        return self.addon.getLocalizedString(code).encode("UTF-8")

from threading import Thread
class InputDialog(Thread):

    def __init__ (self, kodi, request):
        Thread.__init__(self)
        self.kodi = kodi
        self.request = request

    def run(self):
        backup = ""
        value = ""
        id = ""

        # Trata a requisicao
        if "input_num" in self.request:
            id = self.request.replace("input_num_", "")
            backup = self.kodi.mapper.getKeyById(id).getValue()

            value = self.openAnInput(self.kodi.getLocalizedString(32080), backup, True)
        
        elif "input_txt" in self.request:
            id = self.request.replace("input_txt_", "")
            backup = self.kodi.mapper.getKeyById(id).getValue()

            value = self.openAnInput(self.kodi.getLocalizedString(32080), backup)
        
        # Se o campo existe
        if id:
            # Valor nao alterado
            if not value:
                value = backup
            
            # Atualizar os valores
            self.kodi.mapper.getKeyById(id).setValue(value)                
            self.kodi.mapper.setSettingsFields(self.kodi.addon)
            self.kodi.loadSettingsConsts()
            self.kodi.saveSettings()

        self.kodi.setProperty("request_input", "")
        self.kodi.setProperty("response_input", "")

    def openAnInput(self, title, default = "", numeric = False):
        if (numeric):
            return xbmcgui.Dialog().input(title, default, xbmcgui.INPUT_NUMERIC)
        else:
            return xbmcgui.Dialog().input(title, default, xbmcgui.INPUT_ALPHANUM)
