import os
import shutil
import zipfile
import tarfile
import tempfile
from glob import glob


class UncompressFile:
    """Uncompress file."""

    def __init__(self, file_path, tmp_dir):
        """Uncompress file.

        Arg:
            file_path (str): Compressed file path.
            tmp_dir (str): Temporary folder where files will be uncompressed.

        Raise:
            Exception: description

        """
        self.file_path = file_path
        self.tmp_dir = tmp_dir

    def uncompress_targz(self):
        """Uncompress targz file donwloaded."""
        try:
            with tarfile.open(self.image_file_path_targz, "r:gz") as tar:
                tar.extractall(self.dir_tmp_img)
        except Exception:
            print("Error to uncompress targz file")

    def uncompress_zip(self):
        """Uncompress zip file donwloaded."""
        try:
            with zipfile.ZipFile(self.file_path, "r") as zip:
                zip.extractall(self.tmp_dir)
        except Exception:
            print("Error to uncompress zip files")

    def uncompres_file(self, arg):
        """See what extension the file has."""
        if condition:
            pass

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
        self.uncompress_targz()
        if self.check_uncompressed_file():
            self.move_uncompressed_file_wrong_folder()
