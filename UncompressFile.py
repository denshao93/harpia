import os
import shutil
import zipfile
import tarfile
import utils as u
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
            with tarfile.open(self.file_path, "r:gz") as tar:
                tar.extractall(self.tmp_dir)
            if self.check_correct_uncompressed_targz():
                raise Exception
        except Exception:
            print("Wrong place where files where uncompressed.")
            self.move_uncompressed_file_wrong_folder()

    def uncompress_zip(self):
        """Uncompress zip file donwloaded."""
        try:
            with zipfile.ZipFile(self.file_path, "r") as zip:
                zip.extractall(self.tmp_dir)
        except Exception:
            print("Error to uncompress zip files")

    def uncompres_file(self):
        """See what extension the file has."""
        if tarfile.is_tarfile(self.file_path):
            self.uncompress_targz()
        elif zipfile.is_zipfile(self.file_path):
            self.uncompress_zip()

    def check_correct_uncompressed_targz(self):
        """Check if there is .tif files into tmp folder.

        Return:
            [boolean] -- If False the uncompresstion was done corretly
        """
        return len(glob('{}{}'.format(self.tmp_dir, "/*.TIF"))) > 0

    def move_uncompressed_file_wrong_folder(self):
        """Move files to folder named as scene file in tmp folder."""
        file_name = u.get_base_name(self.file_path).split('.')[0]
        files = os.listdir(self.tmp_dir)
        os.mkdir('{}/{}'.format(self.tmp_dir, file_name))
        dst_folder = '{}/{}'.format(self.tmp_dir, file_name)
        for f in files:
            shutil.move(self.tmp_dir+"/"+f, dst_folder)
