import os, sys
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from threading import Thread

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DATA_PATH = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID))
HOME = xbmcgui.Window(10000)

sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')))

from Utils import *

ColorBox_function_map = {
        'blur': blur,
        'pixelate': pixelate,
        'shiftblock': shiftblock,
        'pixelnone': pixelnone,
        'pixelwaves': pixelwaves,
        'pixelrandom': pixelrandom,
        'pixelfile': pixelfile,
        'pixelfedges': pixelfedges,
        'pixeledges': pixeledges,
        'fakelight': fakelight,
        'twotone': twotone,
        'posterize': posterize,
        'distort': distort
}


class ColorBoxMain:

    def __init__(self):
        log("version %s started" % ADDON_VERSION)
        self._init_vars()
        self._parse_argv()
        HOME.setProperty("OldImageColorFIVE", "FF000000")
        HOME.setProperty("ImageColorFIVE", "FFffffff")
        HOME.setProperty("OldImageCColorFIVE", "FF000000")
        HOME.setProperty("ImageCColorFIVE", "FF000000")
        HOME.setProperty("OldImageColorcfa", "FF000000")
        HOME.setProperty("ImageColorcfa", "FF000000")
        HOME.setProperty("OldImageCColorcfa", "FF000000")
        HOME.setProperty("ImageCColorcfa", "FF000000")
        HOME.setProperty("OldImageColorSEVEN", "FF000000")
        HOME.setProperty("ImageColorSEVEN", "FF000000")
        HOME.setProperty("OldImageColorEIGHT", "FF000000")
        HOME.setProperty("ImageColorEIGHT", "FF000000")
        HOME.setProperty("OldImageCColorSEVEN", "FF000000")
        HOME.setProperty("ImageCColorSEVEN", "FF000000")
        HOME.setProperty("OldImageCColorEIGHT", "FF000000")
        HOME.setProperty("ImageCColorEIGHT", "FF000000")
        if not xbmcvfs.exists(ADDON_DATA_PATH):
            # addon data path does not exist...create it
            xbmcvfs.mkdir(ADDON_DATA_PATH)
        if self.infos:
            self._StartInfoActions()
        if self.control == "plugin":
            xbmcplugin.endOfDirectory(self.handle)
        while self.daemon and not xbmc.abortRequested:
            if xbmc.getInfoLabel("ListItem.Property(WatchedEpisodes)") != self.show_watched:
                self.show_watched = xbmc.getInfoLabel("ListItem.Property(WatchedEpisodes)")
                Show_Percentage()
            FIVE_daemon_set = HOME.getProperty("FIVE_daemon_set")
            if not FIVE_daemon_set == 'None':
                self.image_now_FIVE = xbmc.getInfoLabel("Control.GetLabel(7975)")
                if self.image_now_FIVE != self.image_prev_FIVE and self.image_now_FIVE != "":
                    try:
                        self.image_prev_FIVE = self.image_now_FIVE
                        HOME.setProperty("OldImageColorFIVE", HOME.getProperty("ImageColorFIVE"))
                        HOME.setProperty("OldImageCColorFIVE", HOME.getProperty("ImageCColorFIVE"))
                        HOME.setProperty('Daemon_FIVE_ImageUpdating', '0')
                        HOME.setProperty('ImageFilterFIVE', ColorBox_function_map[FIVE_daemon_set](self.image_now_FIVE))
                        HOME.setProperty('ImageFIVE', self.image_now_FIVE)
                        HOME.setProperty('Daemon_FIVE_ImageUpdating', '1')
                        tm1 = Thread(target=Color_Only, args=(self.image_now_FIVE, "ImageColorFIVE", "ImageCColorFIVE"))
                        tm1.start()
                    except:
                        log("Could not process image for cfa daemon")
            cfa_daemon_set = HOME.getProperty("cfa_daemon_set")
            #curr_window = xbmc.getInfoLabel("Window.Property(xmlfile)")
            if not cfa_daemon_set == 'None':
                self.image_now_cfa = xbmc.getInfoLabel("ListItem.Art(fanart)")
                if self.image_now_cfa != self.image_prev_cfa and self.image_now_cfa != "":
                    try:
                        self.image_prev_cfa = self.image_now_cfa
                        HOME.setProperty("OldImageColorcfa", HOME.getProperty("ImageColorcfa"))
                        HOME.setProperty("OldImageCColorcfa", HOME.getProperty("ImageCColorcfa"))
                        HOME.setProperty('DaemonFanartImageUpdating', '0')
                        HOME.setProperty('ImageFiltercfa', ColorBox_function_map[cfa_daemon_set](self.image_now_cfa))
                        HOME.setProperty('DaemonFanartImageUpdating', '1')
                        tf = Thread(target=Color_Only, args=(self.image_now_cfa, "ImageColorcfa", "ImageCColorcfa"))
                        tf.start()
                    except:
                        log("Could not process image for cfa daemon")
            if not HOME.getProperty("SEVEN_daemon_set") == 'None':
                self.image_now_SEVEN = xbmc.getInfoLabel("Control.GetLabel(7977)")
                if self.image_now_SEVEN != self.image_prev_SEVEN and self.image_now_SEVEN != "":
                    try:
                        self.image_prev_SEVEN = self.image_now_SEVEN
                        HOME.setProperty("OldImageColorSEVEN", HOME.getProperty("ImageColorSEVEN"))
                        HOME.setProperty("OldImageCColorSEVEN", HOME.getProperty("ImageCColorSEVEN"))
                        tm3 = Thread(target=Color_Only, args=(self.image_now_SEVEN, "ImageColorSEVEN", "ImageCColorSEVEN"))
                        tm3.start()
                    except:
                        log("Could not process image for SEVEN daemon")
            if not HOME.getProperty("EIGHT_daemon_set") == 'None':
                self.image_now_EIGHT = xbmc.getInfoLabel("Control.GetLabel(7978)")
                if self.image_now_EIGHT != self.image_prev_EIGHT and self.image_now_EIGHT != "":
                    try:
                        self.image_prev_EIGHT = self.image_now_EIGHT
                        HOME.setProperty("OldImageColorEIGHT", HOME.getProperty("ImageColorEIGHT"))
                        HOME.setProperty("OldImageCColorEIGHT", HOME.getProperty("ImageCColorEIGHT"))
                        HOME.setProperty('Daemon_EIGHT_ImageUpdating', '0')
                        HOME.setProperty('ImageFilterEIGHT', ColorBox_function_map[EIGHT_daemon_set](self.image_now_EIGHT))
                        HOME.setProperty('ImageEIGHT', self.image_now_EIGHT)
                        HOME.setProperty('Daemon_EIGHT_ImageUpdating', '1')
                        tm4 = Thread(target=Color_Only, args=(self.image_now_EIGHT, "ImageColorEIGHT", "ImageCColorEIGHT"))
                        tm4.start()
                    except:
                        log("Could not process image for EIGHT daemon")
            xbmc.sleep(200)

    def _StartInfoActions(self):
        for info in self.infos:
            if info == 'randomcolor':
                HOME.setProperty(self.prefix + "ImageColor", Random_Color())
                HOME.setProperty(self.prefix + "ImageCColor", Complementary_Color(HOME.getProperty(self.prefix + "ImageColor")))
            elif info == 'percentage':
                Show_Percentage()
            elif info != '':
                HOME.setProperty(self.prefix + 'ManualImageUpdating', '0')
                HOME.setProperty(self.prefix + 'ImageFilter', ColorBox_function_map[info](self.id))
                HOME.setProperty(self.prefix + 'ManualImageUpdating', '1')
                imagecolor, cimagecolor = Color_Only_Manual(self.id)
                HOME.setProperty(self.prefix + "ImageColor", imagecolor)
                HOME.setProperty(self.prefix + "ImageCColor", cimagecolor)

    def _init_vars(self):
        self.window = xbmcgui.Window(10000)  # Home Window
        self.control = None
        self.infos = []
        self.id = ""
        self.dbid = ""
        self.ptype = "none"
        self.prefix = ""
        self.radius = 10
        self.bits = 2
        self.pixels = 20
        self.container = 518
        self.black = "#000000"
        self.white = "#FFFFFF"
        self.delta_x = 50
        self.delta_y = 90
        self.blocksize = 192
        self.sigma = 0.05
        self.iterations = 1920
        self.daemon = False
        self.show_now = ""
        self.image_now_cfa = ""
        self.image_now_FIVE = ""
        self.image_now_SEVEN = ""
        self.image_now_EIGHT = ""
        self.show_prev = ""
        self.image_prev_cfa = ""
        self.image_prev_FIVE = ""
        self.image_prev_SEVEN = ""
        self.image_prev_EIGHT = ""
        self.show_watched = ""
        self.autoclose = ""

    def _parse_argv(self):
        args = sys.argv
        for arg in args:
            arg = arg.replace("'\"", "").replace("\"'", "")
            if arg == 'script.colorbox':
                continue
            elif arg.startswith('info='):
                self.infos.append(arg[5:])
            elif arg.startswith('id='):
                self.id = RemoveQuotes(arg[3:])
            elif arg.startswith('dbid='):
                self.dbid = int(arg[5:])
            elif arg.startswith('daemon='):
                self.daemon = True
            elif arg.startswith('prefix='):
                self.prefix = arg[7:]
                if not self.prefix.endswith("."):
                    self.prefix = self.prefix + "."
            elif arg.startswith('radius='):
                self.var1 = int(arg[7:])
            elif arg.startswith('pixels='):
                self.var1 = int(arg[7:])
            elif arg.startswith('bits='):
                self.var1 = int(arg[5:])
            elif arg.startswith('black='):
                self.var1 = RemoveQuotes(arg[6:])
            elif arg.startswith('white='):
                self.var2 = RemoveQuotes(arg[6:])
            elif arg.startswith('delta_x='):
                self.var1 = int(arg[8:])
            elif arg.startswith('delta_y='):
                self.var2 = int(arg[8:])
            elif arg.startswith('blocksize='):
                self.var1 = int(arg[10:])
            elif arg.startswith('sigma='):
                self.var2 = int(arg[6:])
            elif arg.startswith('iterations='):
                self.var3 = int(arg[11:])

class ColorBoxMonitor(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        xbmc.Monitor.__init__(self)

    def onPlayBackStarted(self):
        pass
        # HOME.clearProperty(self.prefix + 'ImageFilter')
        # Notify("test", "test")
        # image, imagecolor, cimagecolor = Filter_blur(self.id, self.radius)
        # HOME.setProperty(self.prefix + 'ImageFilter', image)
        # HOME.setProperty(self.prefix + "ImageColor", imagecolor)


if __name__ == "__main__":
    ColorBoxMain()
log('finished')