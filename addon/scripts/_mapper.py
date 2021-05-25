class Key():
    id = ""
    action = ""
    value = ""
    
    def __init__(self, id, action = "", value = ""):
        self.id = id
        self.action = action
        self.value = value

    def getValue(self):
        return self.value

    def setValue(self, value):
        if not value:
            value = ""

        self.value = value 

    def getId(self):
        return self.id

    def setId(self, id):
        if not id:
            id = ""

        self.id = id  

    def getAction(self):
        return self.action

    def setAction(self, action):
        if not action:
            action = ""

        self.action = action  

def getKeyById(id):
    for key in list_keys:
        if key.getId() == id:
            return key

    return ""

def getKeyByValue(value):
    for key in list_keys:
        if key.getValue() == value:
            return key

    return ""

def getKeyByAction(action):
    for key in list_keys:
        if key.getAction() == action:
            return key

    return ""

def setUniqueValue(id, value):
    for key in list_keys:
        if key.getId() == id:
            key.setValue(value)
        elif key.getValue() == value:
            key.setValue("")

def containsId(id):
    if not id:
        return None
    for key in list_keys:
        if key.getId() == id:
            return True
    return False

def containsValue(value):
    if not value:
        return None
    for key in list_keys:
        if key.getValue() == value:
            return True
    return False

def containsAction(action):
    if not action:
        return None
    for key in list_keys:
        if key.getAction() == action:
            return True
    return False

def json_decoder(obj):
    return Key(obj["id"], obj["action"], obj["value"])

def setSettingsFields(addon):
    for key in list_keys:
       addon.setSetting(key.getId(), key.getValue())

# Nao substitui comandos criticos ao estar solicitando tecla
def isBlacklistUpdate(hex):
    key = getKeyByValue(hex)

    if not key:
        return False
    else:
        return (key.getAction() in _blacklist_live_update)

_blacklist_live_update = {
    "Select"
}

list_keys = {
    # Config.
    Key("id",    ""),
    Key("port",  ""),
    Key("desc",  ""),
    Key("state", ""),

    # usuario pode setar esses campos
    Key("pid", "", "FFFF"),
    Key("vid", "", "FFFF"),
    Key("bra", "", "9600"),
    Key("bfi", "", "10"),
    Key("ede", "", "utf-8"),
    Key("tpg", "", "3"),
    Key("tmp", "", "50"),
    Key("tmr", "", "10"),
    Key("tml", "", "10"),
    Key("fcm", "", "IR_"),
    Key("dtc", "", "25"),
    Key("tjt", "", "50"),
    Key("jva", "", "10000"),
    Key("jcf", "", "10140"),

    # teclas
    Key("lef", "Left"),
    Key("rig", "Right"),
    Key("up_", "Up"),
    Key("dow", "Down"),
    Key("sel", "Select"),
    Key("ent", "Enter"),
    Key("pgu", "PageUp"),
    Key("pgd", "PageDown"),
    Key("hgl", "Highlight"),
    Key("pdi", "ParentDir"),
    Key("pmn", "PreviousMenu"),
    Key("bac", "Back"),
    Key("inf", "Info"),
    Key("pau", "Pause"),
    Key("stp", "Stop"),
    Key("skn", "SkipNext"),
    Key("skp", "SkipPrevious"),
    Key("ful", "FullScreen"),
    Key("tfs", "togglefullscreen"),
    Key("ara", "AspectRatio"),
    Key("stf", "StepForward"),
    Key("stb", "StepBack"),
    Key("bsf", "BigStepForward"),
    Key("bsb", "BigStepBack"),
    Key("ssb", "SmallStepBack"),
    Key("csf", "ChapterOrBigStepForward"),
    Key("csb", "ChapterOrBigStepBack"),
    Key("nxs", "NextScene"),
    Key("psc", "PreviousScene"),
    Key("osd", "OSD"),
    Key("dvd", "PlayDVD"),
    Key("svm", "ShowVideoMenu"),
    Key("ssu", "ShowSubtitles"),
    Key("nsu", "NextSubtitle"),
    Key("ssu", "SubtitleShiftUp"),
    Key("ssd", "SubtitleShiftDown"),
    Key("sua", "SubtitleAlign"),
    Key("cif", "CodecInfo"),
    Key("npc", "NextPicture"),
    Key("ppc", "PreviousPicture"),
    Key("zoo", "ZoomOut"),
    Key("zoi", "ZoomIn"),
    Key("ipr", "IncreasePAR"),
    Key("dpr", "DecreasePAR"),
    Key("que", "Queue"),
    Key("pnx", "PlayNext"),
    Key("fil", "Filter"),
    Key("pli", "Playlist"),
    Key("zno", "ZoomNormal"),
    Key("zl1", "ZoomLevel1"),
    Key("zl2", "ZoomLevel2"),
    Key("zl3", "ZoomLevel3"),
    Key("zl4", "ZoomLevel4"),
    Key("zl5", "ZoomLevel5"),
    Key("zl6", "ZoomLevel6"),
    Key("zl7", "ZoomLevel7"),
    Key("zl8", "ZoomLevel8"),
    Key("zl9", "ZoomLevel9"),
    Key("ncl", "NextCalibration"),
    Key("rcl", "ResetCalibration"),
    Key("amv", "AnalogMove"),
    Key("rot", "Rotate"),
    Key("rcc", "rotateccw"),
    Key("clo", "Close"),
    Key("sdy", "subtitledelay"),
    Key("sdm", "SubtitleDelayMinus"),
    Key("sdp", "SubtitleDelayPlus"),
    Key("ady", "audiodelay"),
    Key("adm", "AudioDelayMinus"),
    Key("adp", "AudioDelayPlus"),
    Key("anl", "AudioNextLanguage"),
    Key("nxr", "NextResolution"),
    Key("ffw", "FastForward"),
    Key("rew", "Rewind"),
    Key("pla", "Play"),
    Key("ppa", "PlayPause"),
    Key("del", "Delete"),
    Key("cop", "Copy"),
    Key("mov", "Move"),
    Key("ren", "Rename"),
    Key("hsm", "HideSubmenu"),
    Key("sct", "Screenshot"),
    Key("vlu", "VolumeUp"),
    Key("vld", "VolumeDown"),
    Key("mut", "Mute"),
    Key("vau", "volampup"),
    Key("vad", "volampdown"),
    Key("atd", "audiotoggledigital"),
    Key("bsp", "BackSpace"),
    Key("sup", "ScrollUp"),
    Key("sdo", "ScrollDown"),
    Key("aff", "AnalogFastForward"),
    Key("are", "AnalogRewind"),
    Key("asf", "AnalogSeekForward"),
    Key("asb", "AnalogSeekBack"),
    Key("miu", "MoveItemUp"),
    Key("mid", "MoveItemDown"),
    Key("men", "Menu"),
    Key("cme", "ContextMenu"),
    Key("shi", "Shift"),
    Key("sym", "Symbols"),
    Key("cle", "CursorLeft"),
    Key("cri", "CursorRight"),
    Key("sti", "ShowTime"),
    Key("vpl", "visualisationpresetlist"),
    Key("sps", "ShowPreset"),
    Key("nps", "NextPreset"),
    Key("pps", "PreviousPreset"),
    Key("lpr", "LockPreset"),
    Key("rpr", "RandomPreset"),
    Key("ira", "IncreaseRating"),
    Key("dra", "DecreaseRating"),
    Key("twa", "ToggleWatched"),
    Key("nle", "NextLetter"),
    Key("ple", "PrevLetter"),
    Key("vsu", "verticalshiftup"),
    Key("vsd", "verticalshiftdown"),
    Key("sit", "scanitem"),
    Key("rke", "reloadkeymaps"),
    Key("ivr", "increasevisrating"),
    Key("dvr", "decreasevisrating"),
    Key("fpa", "firstpage"),
    Key("lpa", "lastpage"),
    Key("gpr", "guiprofile"),
    Key("red", "red"),
    Key("gre", "green"),
    Key("yel", "yellow"),
    Key("blu", "blue"),
    Key("cbo", "CreateBookmark"),
    Key("ceb", "CreatEpisodeBookmark"),
    Key("ncg", "NextChannelGroup"),
    Key("pcg", "PreviousChannelGroup"),
    Key("cup", "ChannelUp"),
    Key("cdo", "ChannelDown"),
    Key("ppv", "PlayPvr"),
    Key("ppt", "PlayPvrTV"),
    Key("ppr", "PlayPvrRadio"),
    Key("rec", "Record"),
    Key("smo", "StereoMode"),
    Key("sra", "SetRating"),
    Key("ulv", "UpdateLibrary(video)"),
    Key("shu", "Powerdown"),

    Key("sp1", "Seek(25)"),
    Key("sp2", "Seek(50)"),
    Key("sp3", "Seek(75)"),
    Key("sp4", "Seek(100)"),
    Key("sp5", "Seek(-25)"),
    Key("sp6", "Seek(-50)"),
    Key("sp7", "Seek(-75)"),
    Key("sp8", "Seek(-100)"),
    Key("nu0", "Number0"),
    Key("nu1", "Number1"),
    Key("nu2", "Number2"),
    Key("nu3", "Number3"),
    Key("nu4", "Number4"),
    Key("nu5", "Number5"),
    Key("nu6", "Number6"),
    Key("nu7", "Number7"),
    Key("nu8", "Number8"),
    Key("nu9", "Number9"),
    Key("js2", "JumpSMS2"),
    Key("js3", "JumpSMS3"),
    Key("js4", "JumpSMS4"),
    Key("js5", "JumpSMS5"),
    Key("js6", "JumpSMS6"),
    Key("js7", "JumpSMS7"),
    Key("js8", "JumpSMS8"),
    Key("js9", "JumpSMS9"),
    Key("fs2", "FilterSMS2"),
    Key("fs3", "FilterSMS3"),
    Key("fs4", "FilterSMS4"),
    Key("fs5", "FilterSMS5"),
    Key("fs6", "FilterSMS6"),
    Key("fs7", "FilterSMS7"),
    Key("fs8", "FilterSMS8"),
    Key("fs9", "FilterSMS9"),
    
    # System bultin
    Key("asc", "system_b_ActivateScreensaver"),
    Key("hib", "system_b_Hibernate"),
    Key("iit", "system_b_InhibitIdleShutdown(true)"),
    Key("iif", "system_b_InhibitIdleShutdown(false)"),
    Key("miz", "system_b_Minimize"),
    Key("pwd", "system_b_Powerdown"),
    Key("qui", "system_b_Quit"),
    Key("roo", "system_b_Reboot"),
    Key("res", "system_b_Reset"),
    Key("rap", "system_b_RestartApp"),
    Key("std", "system_b_ShutDown"),
    Key("sus", "system_b_Suspend"),
}