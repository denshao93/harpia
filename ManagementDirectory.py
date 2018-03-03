import os
from glob import glob


def get_targz_files_from_folder(folder):
    """
    Getting list of tar.gz files in folders recursively
    :return: list of tar.gz files
    """
    return glob('{}{}'.format(folder, '/*tar.gz'), recursive=True)


def get_folder_name(folder):

    return glob(folder, recursive=True)


def get_list_folder_name_from_processed_dir(folder):

    list_folder = glob('{}{}'.format(folder, '/*/'))
    list_folder_name = [i.split('/')[-2] for i in [i.split(',')[0] for i in list_folder]]
    return list_folder_name









