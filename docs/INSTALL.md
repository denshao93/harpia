# Setting Python 3 enviroment 

___________________________________________________

All settings were done in Linux Mint 19.1 with Ubuntu 18.04.

## Install pyenv
### It separate harpia enviroment from system enviroment in order to don't break linux's behavior.

For more help, see documentation in:

[GitHub of pyenv](http://github.com/pyenv/pyenv)

```bash
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
```

Settings of pyenv in order to bash can recognize its commands.
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
```

Update bashrc to able pyenv commands works in bash
```bash
source $HOME/.bashrc
```

Create python 3 enviroment with pyenv


```bash
pyenv install 3.7.3
pyenv global 3.7.3
```

Install virtualenv and virtualwrapper

```bash
pip install virtualenv virtualenvwrapper
```

Create dictory to save virtual enviroment of python

```bash
mkdir ~/.ve
mkdir ~/workspac/harpia
mkvirtualenv harpia -a ~/workspace/harpia/app
```

## Install gdal in VirtualEnvironment

Gdal needs to support hdf5 format file to gdal-segment

```c

sudo apt-get install libgdal-dev g++ gdal-bin python-gdal python3-gdal
workon harpia
pip install pygdal==2.2.3

```

Obs: Pay attention to pygdal version. It need to be the same as system installed
___________________________________________________

## Install OpenCV

```c

Ubuntu 16.04
sudo apt-get install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

Ubuntu 18.04
sudo apt install build-essential cmake git pkg-config libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev gfortran openexr python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev


mkdir src && cd src && git clone https://github.com/opencv/opencv.git
git checkout 3.4.2
cd src/opencv
git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.4.2
mkdir build && cd build



Ubuntu 18.04
https://www.pyimagesearch.com/2018/05/28/ubuntu-18-04-how-to-install-opencv/

cmake -D CMAKE_BUILD_TYPE=RELEASE \
	-D CMAKE_INSTALL_PREFIX=/usr/local \
	-D INSTALL_PYTHON_EXAMPLES=ON \
	-D INSTALL_C_EXAMPLES=OFF \
	-D OPENCV_ENABLE_NONFREE=ON \
	-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
	-D PYTHON_EXECUTABLE=~/.ve/harpia/bin/python \
	-D BUILD_EXAMPLES=ON ..


Ubuntu 16.04

cmake CMAKE_VERBOSE=1 -D CMAKE_INSTALL_PREFIX=/usr/local -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -DPYTHON_EXECUTABLE=/home/diogocaribe/.ve/harpia/bin/python -DCMAKE_SKIP_RPATH=ON ../

sudo cmake CMAKE_VERBOSE=1 -D OPENCV_EXTRA_MODULES_PATH=/home/diogocaribe/src/opencv_contrib/modules -DCMAKE_SKIP_RPATH=ON ../
make -j4
sudo make install
sudo ldconfig

```

___________________________________________________

## Install gdal-segment

```c

git clone https://github.com/cbalint13/gdal-segment.git
cd gdal-segment && mkdir build && cd build
cmake ../
sudo make

```

## Install fmask

```c

cd ~/Downloads
workon harpia
wget 'https://bitbucket.org/chchrsc/rios/downloads/rios-1.4.6.tar.gz'
wget 'https://bitbucket.org/chchrsc/python-fmask/downloads/python-fmask-0.5.2.tar.gz'
tar -xvzf rios-1.4.6.tar.gz
tar -xvzf python-fmask-0.5.2.tar.gz

workon harpia
cd rios-1.4.6 && python setup.py install
cd python-fmask-0.5.2 && python setup.py install

```