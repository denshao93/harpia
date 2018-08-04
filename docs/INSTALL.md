# Setting enviroment

___________________________________________________

## Install dependecies to pyenv

```c
sudo apt install curl git-core gcc make zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libssl-dev
```

## Install pyenv

```c
git clone https://github.com/pyenv/pyenv.git $HOME/.pyenv
```

## pyenv configs

```c
nano $HOME/.bashrc
```

Copy and paste at the end of bashrc

```c
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
eval "$(pyenv init -)"
fi
```

Save file

```c
source $HOME/.bashrc
```

## Install pyenv-virtualenv

```c
git clone https://github.com/yyuu/pyenv-virtualenv.git   $HOME/.pyenv/plugins/pyenv-virtualenv
```

## Install python with pyenv

```c
pyenv install 3.6.6
```

```c
pyenv global 3.6.6
```

## Directory architecture

```c
mkdir ~/.ve
"Project code is in:"
mkdir ~/workspace
```

## Install virtualenvwrapper

```c

git clone https://github.com/pyenv/pyenv-virtualenvwrapper.git $(pyenv root)/plugins/pyenv-virtualenvwrapper

pip install virtualenv virtualenvwrapper
```

## Open terminal

```c
nano $HOME/.bashrc

export WORKON_HOME=~/.ve
export PROJECT_HOME=~/workspace
pyenv virtualenvwrapper_lazy


Save file

source ~/.bashrc
bash

```

## Connect workspace to virtual environment

```c

mkvirtualenv -a ~/workspace/harpia/app harpia

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
sudo apt-get install build-essential
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev


Ubuntu 18.04
sudo apt install build-essential cmake git pkg-config libgtk-3-dev
sudo apt install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev
sudo apt install libjpeg-dev libpng-dev libtiff-dev gfortran openexr
sudo apt install python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev


mkdir /src
cd src
git clone https://github.com/opencv/opencv.git
git checkout 3.4.2
cd src/openvc
git clone https://github.com/opencv/opencv_contrib.git
git checkout 3.4.2
mkdir build && cd build

Ubuntu 18.04
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..

cmake CMAKE_VERBOSE=1 -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules -DCMAKE_SKIP_RPATH=ON ../
make -j4
sudo make install

```

___________________________________________________

## Install gdal-segment

```c

git clone https://github.com/cbalint13/gdal-segment.git
cd gdal-segment && mkdir build && cd build
cmake ../
sudo make

```