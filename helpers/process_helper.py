import datetime
import os

class ProcessHelper:

    def get_folder_name(self,root):
        dt = datetime.datetime.now()
        ft = dt.strftime("%d_%b_%Y_(%H_%M_%S)")
        pt = root + "/" + ft

    def make_folder(self,path):
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
        return path

    def make_folder_by_detail(self,detail_code):
        pass
