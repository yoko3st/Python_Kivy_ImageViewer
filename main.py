from xml.dom.pulldom import PROCESSING_INSTRUCTION
from kivy.config import Config
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'resizable', 1)

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty

from pathlib import Path
from kivy.modules import keybinding
from kivy.core.window import Window

import re
from natsort import natsorted
import sys

def paths_sorted(paths):
    return natsorted(paths, key = lambda x: str(x.name))

class ImageWidget(Widget):
    global gazou_list_key
    global gazou_list
    gazou_list_key = 0
    gazou_list = []
    
    if(len(sys.argv) <= 1):
        print("This program expects an image file(.jpg,.gif.png) as an argument.")
        sys.exit()
    else:
        args = sys.argv
        file_mei = args[1]
        kakuchoushi = file_mei[-4:]
        if any([kakuchoushi == ".jpg", kakuchoushi == ".gif", kakuchoushi == ".png"]):
            pass
        else:
            print("This program expects an image file(.jpg,.gif.png) as an argument.")
            sys.exit()

    file_mei_re = re.sub(r"\\","/",str(file_mei))
    file_path = Path(file_mei_re)
    for image_file in paths_sorted(list(Path(file_path.parent).iterdir())):
        kakuchoushi = image_file.suffix
        if any([kakuchoushi == ".jpg", kakuchoushi == ".gif", kakuchoushi == ".png"]):
            imanogazou = re.sub(r"\\","/",str(image_file))
            gazou_list.append(imanogazou)

    for k, v in enumerate(gazou_list):
        if (v == file_mei_re):
            gazou_list_key = k
            break
    source = StringProperty(gazou_list[gazou_list_key])

    def __init__(self, **kwargs):
        super(ImageWidget, self).__init__(**kwargs)
        Window.bind(on_key_down=self.key_action)

    def key_action(self, *args):
        # left：276、right：275、a：97、d：100
        # print(args)
        # print(args[1])
        global gazou_list_key
        if (args[1] == 276) or (args[1] == 97):
            if(gazou_list_key != 0):
                gazou_list_key -= 1
            else:
                gazou_list_key = len(gazou_list)-1
        if (args[1] == 275) or (args[1] == 100):
            if(gazou_list_key != (len(gazou_list)-1)):
                gazou_list_key += 1
            else:
                gazou_list_key = 0
        self.source = gazou_list[gazou_list_key]

class GazouApp(App):
    def __init__(self, **kwargs):
        super(GazouApp, self).__init__(**kwargs)
        self.title = 'ImageViewer'

if __name__ == '__main__':
    GazouApp().run()