import os
from glob import glob
import tarfile


class HandleImageDirectory:

    def __init__(self, folder):
        self.folder = folder

    def get_targz_files(self):

        return glob('{}{}'.format(self.folder, '/*tar.gz'), recursive=True)

    def get_tmp_folder(self):

        dir_list = glob("~/")

        if '{}{}'.format(dir_list, '/tmp/') not in dir_list:
            os.mkdir('{}{}'.format(dir_list, '/tmp/'))
            return True


    def del_tmp_folder(self):

        os.rmdir('~/tmp')

    def run(self):
        self.get_tmp_folder()
        return self.get_targz_files()




