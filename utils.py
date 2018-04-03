import os
import tarfile


def file_name_without_extention(file_path):

    basename = os.path.basename(file_path)

    file_name = basename.split('.')[0]

    return file_name


def uncompress_image_bands_from_0_to_9(file_path):

    def bands_0_to_9(members):
        for tarinfo in members:
            if os.path.splitext(tarinfo.name)[1] == "LC08*_B[1-7,9].TIF":
                yield tarinfo

    tar = tarfile.open(file_path)
    tar.extractall(path='/tmp/', members=bands_0_to_9(tar))
    tar.close()


if __name__ == "__main__":

    uncompress_image_bands_from_0_to_9("/media/dogosousa/1AF3820C0AA79B17/BRUTA/LC8/"
                                       "215068/LC08_L1TP_215068_20151114_20170402_01_T1.tar.gz")
