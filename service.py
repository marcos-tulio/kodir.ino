if __name__ == '__main__':
    import xbmcaddon, os

    _addon = xbmcaddon.Addon()
    scripts  = os.path.join(_addon.getAddonInfo('path').decode('utf-8'), 'scripts')

    from scripts import _main as Main

    Main.kodi.loadSettings()
    Main.kodi.setDisconnected()

    # Carrega as constantes 
    Main.kodi.loadSettingsConsts()

    Main.kodi.enableMonitor()
    Main.Controller().run()
