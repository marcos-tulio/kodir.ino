import sys
import xbmcaddon

addon = xbmcaddon.Addon()

if len(sys.argv) > 1:
    import os
    scripts = os.path.join(addon.getAddonInfo('path'), 'scripts')
    from scripts import _main as Main

    item_id = sys.argv[1]

    if ("input_" in item_id) and (not Main.kodi.getProperty("request_input")):
        Main.kodi.setProperty("request_input", item_id)

    elif "key_" in item_id:
        Main.kodi.loadSettings(False)
        Main.kodi.loadSettingsConsts()
        Main.kodi.addonSelectKey(item_id.replace("key_", ""))

elif __name__ == '__main__':
    import xbmcgui
    xbmcgui.Dialog().ok(addon.getAddonInfo('name'), addon.getLocalizedString(32060))

