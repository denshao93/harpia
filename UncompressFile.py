import os
import shutil
import tarfile
import tempfile
from glob import glob


class UncompressFile:
    """Uncompress tar.gz file"""

    def __init__(self, image_file_path_targz, file_name):
        """
        Arguments:
            image_file_path_targz {str} -- [description]
            file_name {str} -- [description]
        """
        # Input row file (landsat file compressed like dowloaded from USGS)
        self.image_file_path_targz = image_file_path_targz

        # Temporary folder to put files to process and remove after that
        self.tmp = tempfile.gettempdir()

        # Tmp directory to put landsat imagens
        self.dir_tmp_img = tempfile.mkdtemp()

        # File name
        self.file_name = file_name

    def uncompress_img(self):
        """This function uncompress tar.gz files donwloaded from USGS"""
        try:
            with tarfile.open(self.image_file_path_targz, "r:gz") as tar:
                tar.extractall(self.dir_tmp_img)
        except:
            print("Error to uncompress image files")

    def check_uncompressed_file(self):
        """Check if there is .tif files into tmp folder.
        Returns:
            [boolean] -- If False the uncompresstion was done corretly
        """
        return len(glob('{}{}'.format(self.dir_tmp_img, "/*.TIF"))) > 0

    def move_uncompressed_file_wrong_folder(self):
        """If image files were uncompressed in wrong place, this method will put it
        in place where all of code recognized
        """
        files = os.listdir(self.dir_tmp_img)
        os.mkdir('{}/{}'.format(self.dir_tmp_img, self.file_name))
        dst_folder = '{}/{}'.format(self.dir_tmp_img, self.file_name)

        for f in files:
            shutil.move(self.dir_tmp_img+"/"+f, dst_folder)

    @staticmethod
    def close_tmp_dir(dir_path):
        shutil.rmtree(dir_path)

    def run(self):
        self.uncompress_img()
        if self.check_uncompressed_file():
            self.move_uncompressed_file_wrong_folder()

# Exemple
# if __name__ == '__main__':

#     file = UncompressFile("/media/diogocaribe/56A22ED6A22EBA7F/BRUTA/LC8/215068/LC08_L1TP_215068_20171205_20171222_01_T1.tar.gz",
#     "LC08_L1TP_215068_20171205_20171222_01_T1")
#     file.run()
    # file = UncompressFile("/media/diogocaribe/56A22ED6A22EBA7F/BRUTA/LC8/215068/LC08_L1TP_215068_20160913_20170321_01_T1.tar.gz")
    # file.run()


