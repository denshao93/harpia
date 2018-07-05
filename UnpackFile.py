import os
import re
import shutil
import zipfile
import tarfile
import utils as u
from glob import glob


class UnpackFile:
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
        except Exception:
            print("Wrong place where files where uncompressed.")

    def uncompress_zip(self):
        """Uncompress zip file donwloaded."""
        try:
            with zipfile.ZipFile(self.file_path, "r") as zip:
                zip.extractall(self.tmp_dir)
        except Exception:
            print("Error to uncompress zip files")

    def unpack_landsat(self, bands):
        """
        Function to unpack a landsat archive (.tar.gz) to a
        specified output directory.
        This function makes the assumption that the archive is
        ordered by band and that the last file is a metadata file.
        Arguments:
            inpath: Full path to landsat archive (.tar.gz extention)
            outpath: Full path to an outup directory in which to place the
                extracted files from the inpath archive.
            bands: list of bands to extract from the archive. Default = all.
        Output:
            Unpacked landsat archive to the outpath directory
        """
        tfile = tarfile.open(self.file_path,'r:gz')
        #Extract just the bands specified.

        #Get the names of the members of the archive
        names = tfile.getnames()

        #Make sure the bands are given as a list
        bands = list(bands)

        #Find those elements of the archive that match the bands specified
        #	(plus metadata file)
        members = tfile.getmembers()
        elements = []
        blist = ''.join(str(i) for i in bands)
        patternStr =    '.*_B[' + blist + ']\.TIF|' + \
                        '.*_B1[' + blist + ']\.TIF|.*_MTL*\.txt'

        pattern = re.compile(patternStr)
        for i, name in enumerate(names):
            if pattern.match(name):
                    elements.append(members[i])
        tfile.extractall(self.tmp_dir, members = elements)
        tfile.close()

    def uncompres_file(self, bands):
        """See what extension the file has."""
        if tarfile.is_tarfile(self.file_path):
            self.unpack_landsat(bands)
        elif zipfile.is_zipfile(self.file_path):
            self.uncompress_zip()

    def check_correct_uncompressed_targz(self):
        """Check if there is .tif files into tmp folder.

        Return:
            [boolean] -- If False the uncompresstion was done corretly
        """
        return len(glob('{}{}'.format(self.tmp_dir, "/*.TIF"))) > 0

    def move_file_2_right_folder(self):
        """Move files to folder named as scene file in tmp folder."""
        file_name = u.get_base_name(self.file_path).split('.')[0]
        files = os.listdir(self.tmp_dir)
        os.mkdir('{}/{}'.format(self.tmp_dir, file_name))
        dst_folder = '{}/{}'.format(self.tmp_dir, file_name)
        for f in files:
            shutil.move(self.tmp_dir+"/"+f, dst_folder)
