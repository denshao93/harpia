Welcome to the preprocess2ta wiki!

Instalando o OpenCV

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install build-essential cmake pkg-config

# Libs para leitura de imagens (não instalei as libs para leitura de videos e a interface gráfica)
sudo apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev

###### Libs para videos (não instaladas pq só trabalharemos com imagens)
# sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
# sudo apt-get install libxvidcore-dev libx264-dev

sudo apt-get install libgtk-3-dev

sudo apt-get install libatlas-base-dev gfortran

sudo apt-get install python2.7-dev python3.5-dev

################## Download OpenCV ###################
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.4.1.zip
unzip opencv.zip

wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.4.1.zip
unzip opencv_contrib.zip

######################################################
sudo apt-get install python3-pip python-pip
sudo pip3 install pip==9.0.3
sudo pip install pip==9.0.3

# Criando o ambiente virtual
sudo pip install virtualenv virtualenvwrapper
sudo rm -rf ~/.cache/pip

cd ~
nano .bashrc

# virtualenv and virtualenvwrapper
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

source ~/.bashrc

# Criando o ambiente (env) na pasta do projeto (isolado do SO)
Este ambiente não é necessario para rodar o gdal-segment. 
A compilação do OpenCV desse modo permite rodar as funções do da lib atraves do python.
# Atentar para fazer a pasta na pasta do projeto

#Por algum montivo o pip==10.0.1 ta sendo instalado no virtualenv
#Realizar o downgrade para o 9.0.3 pois o 10 esta com um bug que não consegui desvendar
mkvirtualenv env -p python3

pip3 install numpy

cmake CMAKE_VERBOSE=1 -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D INSTALL_C_EXAMPLES=OFF \
      -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.4.1/modules \
      -D PYTHON_EXECUTABLE=~/.virtualenvs/env/bin/python \
      -D CMAKE_SKIP_RPATH=ON \
      -D BUILD_EXAMPLES=ON ..

# Definir o numero de núcleos utilizados para a compilação.
make -j6

sudo make install
sudo ldconfig

cd /usr/local/lib/python3.5/site-packages/
ls -l

sudo mv cv2.cpython-35m-x86_64-linux-gnu.so cv2.so

cd ~/.virtualenvs/env/lib/python3.5/site-packages/
ln -s /usr/local/lib/python3.5/site-packages/cv2.so cv2.so

ex.
import cv2