import re
import os
import tarfile


def check(string):
    # Explicação para a expressão regular
    # ^ = irá procurar a partir do inicio da string a ser comparada
    # .* = capturar todos os caracteres
    m = re.match("^LC08.*_B[1-7,9]", string)
    print(m)
    return m


# def py_files(members):
#     for tarinfo in members:
#         string = os.path.splitext(tarinfo.name)[0].split('/')[1]
#         print(string)
#         if check(string) is not None:
#             yield tarinfo
#
#
# tar = tarfile.open("/media/dogosousa/1AF3820C0AA79B17/BRUTA/LC8/215068/"
#                    "LC08_L1TP_215068_20151114_20170402_01_T1.tar.gz")
# tar.extractall(path="/tmp/", members=py_files(tar))
# tar.close()

def extract_bands():

    try:
        t = tarfile.open("/media/dogosousa/1AF3820C0AA79B17/BRUTA/LC8/215068/"
                         "LC08_L1TP_215068_20151114_20170402_01_T1.tar.gz", 'r')
    except IOError as e:
        print(e)
    else:
        # t.extractall("/tmp/", members=[m for m in t.getmembers() if check())
        pass


if __name__ == "__main__":
    extract_bands()
