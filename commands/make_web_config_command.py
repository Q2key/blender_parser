import os
import json
from PIL import Image

from helpers.process import ProcessHelper
from commands.scan_store_command import ScanStoreCommand

class MakeWebConfigCommand(ScanStoreCommand):


    def saveThumb(self, file):
        try:
            im = Image.open(file['texture'])

            new_width  = 200
            new_height = 200
            
            im = im.resize((new_width, new_height), Image.ANTIALIAS)
            pth = '{0}/{1}.png'.format(self.ctx.THUMBS_PATH,file['id'])
            im.save(pth)
        
        except IOError:
            pass

    def saveAllThumbs(self, files):
        for f in files:
            self.saveThumb(f)

    def run(self):
        self.search_for_material()
        self.update_config()

        mts = self.search_for_material()
        data = json.dumps(mts, sort_keys=True, indent=4)
        
        self.saveAllThumbs(mts)
        self.write_config("{0}/render.json".format(self.ctx.CONFIG_PATH),data)



